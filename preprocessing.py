from typing import List
from random import shuffle
from itertools import chain

from tqdm.notebook import tqdm


class Dialog:
    def __init__(self, dialogs: List[str], history_size=2, speaker1_token='<speaker1>', speaker2_token='<speaker2>',
                 bos_token='<bos>', eos_token='<eos>'):
        self.dialogs = dialogs
        self.speaker1_token = speaker1_token
        self.speaker2_token = speaker2_token
        self.history_size = history_size
        self.bos_token = bos_token
        self.eos_token = eos_token

        self.result_texts = None

    def preprocess_for_raw_text(self, dialog: str) -> str:
        dialog = dialog.replace('<br />', ' ').replace('</span> ', '')
        dialog = dialog.replace('<span class=participant_1>Пользователь 1: ', self.speaker1_token )
        dialog = dialog.replace('<span class=participant_2>Пользователь 2: ', self.speaker2_token )
        return dialog

    def form_raw_text(self, dialog: str) -> List[str]:
        res = []
        speaker_token_len = len(self.speaker1_token)
        prev_speaker = dialog[: speaker_token_len]
        for ind, char in enumerate(dialog):
            if char == self.speaker1_token[0] and dialog[ind:ind + speaker_token_len] != prev_speaker:
                res.append('\n')
                prev_speaker = ''.join(dialog[ind:ind + speaker_token_len])
            res.append(char)
        return ''.join(res).split('\n')

    def get_chunks(self, dialog, use_history=True):
        result = list()

        if use_history:
            for i in range(self.history_size, len(dialog) + 1):
                if i <= self.history_size * 2:
                    result.append(dialog[:i])
                else:
                    result.append(dialog[i - self.history_size * 2: i])
        else:
            result.append([self.bos_token] + self.form_raw_text(dialog) + [self.eos_token])
        return result

    def form_data_to_train(self):
        result = []
        for dialog in tqdm(self.dialogs):
            replicas = self.get_chunks(self.form_raw_text(dialog))
            result.extend([[self.bos_token] + dialog + [self.eos_token] for dialog in replicas])
        return result


class DialogWithCharacter(Dialog):
    def __init__(self, dialogs: List[str],
                 persona1_characteristics: List[List[str]], persona2_characteristics: List[List[str]],
                 history_size=2, speaker1_token='<speaker1>', speaker2_token='<speaker2>', person_token='<person>',
                 bos_token='<bos>', eos_token='<eos>'):
        super(DialogWithCharacter, self).__init__(dialogs, history_size,
                                                  speaker1_token, speaker2_token,
                                                  bos_token, eos_token)
        self.persona1_characteristics = persona1_characteristics
        self.persona2_characteristics = persona2_characteristics
        self.person_token=person_token

    def include_all_in_dialog(self, history_and_replica, include_persona=False, persona_1=None, persona_2=None):
        result = list()
        for replica in history_and_replica:
            if include_persona:
                if replica[-1][:10] == self.speaker1_token:
                    shuffle(persona_1)
                    person = persona_1
                else:
                    shuffle(persona_2)
                    person = persona_2
                result.append(' '.join(chain([self.bos_token] + [self.person_token] + person + replica + [self.eos_token])))
            else:
                result.append(' '.join([self.bos_token] + replica + [self.eos_token]))
        return result

    def form_data_to_train(self, include_person=True):
        result = []
        iterator = zip(self.dialogs, self.persona2_characteristics, self.persona2_characteristics)
        for chunk in tqdm(iterator):
            dialog, per_1, per_2 = chunk
            replicas = self.include_all_in_dialog(self.get_chunks(self.form_raw_text(dialog)),
                                                  include_person, per_1, per_2)
            result.extend(replicas)
        return result
