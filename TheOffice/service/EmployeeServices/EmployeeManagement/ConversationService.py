import random

from pygame import time

from model.Employee.Employee import Employee

DISAGREE_SPEECH_BUBBLE_INDEX = 0


class ConversationService:
    def __init__(self, employee_list, animation_box: dict):
        self.employee_list = employee_list
        self.LETS_TALK = 4
        self.conversation_pairs = []
        self.argument_pairs = []
        self.fight_pairs = []
        self.FIRST_SPEAK = 1500
        self.SECOND_SPEAK = 3000
        self.END_SPEAK = 8000
        self.ARGUE_LEVEL = - 15
        self.FIGHT_LEVEL = - 30
        self.conversation_result_list = []
        self.animation_box = animation_box

    def manage_emps_conversations(self):
        for emp in self.employee_list:
            for emp2 in self.employee_list:
                emp.vision_field.x = emp.rect.x - 50
                emp.vision_field.y = emp.rect.y
                emp2.vision_field.x = emp2.rect.x - 50
                emp2.vision_field.y = emp2.rect.y
                if emp != emp2 and self.emps_are_passing_by(emp, emp2):
                    conversation_chances = random.randrange(1, 150)
                    if conversation_chances == self.LETS_TALK:
                        if not emp.has_relation_with(emp2):
                            emp.relations.update({emp2: 0})
                            emp2.relations.update({emp: 0})
                        if emp.relations.get(emp2) <= self.FIGHT_LEVEL:
                            self.initiate_fight(emp, emp2)
                        elif emp.relations.get(emp2) <= self.ARGUE_LEVEL:
                            self.initiate_argument(emp, emp2)
                        else:
                            self.initiate_conversation(emp, emp2)

    def make_emps_converse(self):
        for pair in self.conversation_pairs[:]:
            if self.check_convo_phase(pair.conversation_timestamp, self.FIRST_SPEAK):
                pair.trigger_current_start_topic_speech_bubble_once()
                pair.attach_current_start_topic_speech_bubble_to_emp()
            elif self.check_convo_phase(pair.conversation_timestamp, self.SECOND_SPEAK):
                pair.trigger_current_respond_speech_bubble_once()
                pair.attach_current_respond_speech_bubble_to_emp()
            else:
                pair.finish_topic()
                if pair.is_last_topic():
                    pair.unblock_movement()
                    if not self.check_convo_phase(pair.conversation_timestamp, self.END_SPEAK):
                        pair.emp1.in_interaction = False
                        pair.emp2.in_interaction = False
                        pair.emp1.needs.play()
                        pair.emp1.needs.meet()
                        pair.emp2.needs.play()
                        pair.emp2.needs.meet()
                        self.update_emp_relationships(pair, sum(pair.emps_agree_on_topic_list))
                        self.conversation_pairs.remove(pair)
                else:
                    pair.next_topic()
                    pair.swap_conversation_roles()

    def make_emps_argue(self):
        for pair in self.argument_pairs[:]:
            if self.check_convo_phase(pair.argument_timestamp, self.FIRST_SPEAK):
                pair.trigger_current_start_argument_bubble_once()
                pair.attach_current_start_argument_bubble_to_emp()
            elif self.check_convo_phase(pair.argument_timestamp, self.SECOND_SPEAK):
                pair.trigger_current_respond_argument_bubble_once()
                pair.attach_current_respond_argument_bubble_to_emp()
            else:
                pair.finish_argument()
                pair.unblock_movement()
                if not self.check_convo_phase(pair.argument_timestamp, self.END_SPEAK):
                    pair.emp1.in_interaction = False
                    pair.emp2.in_interaction = False
                    pair.emp1.needs.decrease_stress()
                    pair.emp1.needs.decrease_motivation()
                    pair.emp2.needs.decrease_stress()
                    pair.emp2.needs.decrease_motivation()
                    self.update_emp_relationships(pair, pair.relation_penalty)
                    self.argument_pairs.remove(pair)

    def make_emps_fight(self):
        for pair in self.fight_pairs[:]:
            if self.check_convo_phase(pair.fight_timestamp, self.FIRST_SPEAK):
                pair.trigger_fight_animation_once()
                pair.attach_fight_cloud_to_emp()
            else:
                pair.finish_fight()
                pair.unblock_movement()
                if not self.check_convo_phase(pair.fight_timestamp, self.END_SPEAK):
                    pair.emp1.in_interaction = False
                    pair.emp2.in_interaction = False
                    pair.emp1.needs.decrease_stress()
                    pair.emp1.needs.decrease_motivation()
                    pair.emp2.needs.decrease_stress()
                    pair.emp2.needs.decrease_motivation()
                    self.update_emp_relationships(pair, pair.relation_penalty)
                    self.fight_pairs.remove(pair)

        # stop conversation animations

    def emps_are_passing_by(self, emp, emp2):
        return (emp.is_emp_in_vision(emp2)
                and not (emp.in_interaction or emp2.in_interaction or emp2.is_working()
                         or emp.is_working() or emp2.is_peeing() or emp.is_peeing() or emp.is_in_need() or emp2.is_in_need()))

    def initiate_conversation(self, emp: Employee, emp2: Employee):
        emp.in_interaction = True
        emp2.in_interaction = True
        emp.block_move = True
        emp2.block_move = True
        self.conversation_pairs.append(ConversationPair(emp, emp2, self.animation_box))

    def check_convo_phase(self, conversation_timestamp, speak_phase):
        return time.get_ticks() - conversation_timestamp < speak_phase

    def update_emp_relationships(self, pair, result):
        pair.emp1.relations.update({pair.emp2: pair.emp1.relations.get(pair.emp2) + result})
        pair.emp2.relations.update({pair.emp1: pair.emp2.relations.get(pair.emp1) + result})

    def initiate_argument(self, emp, emp2):
        emp.in_interaction = True
        emp2.in_interaction = True
        emp.block_move = True
        emp2.block_move = True
        self.argument_pairs.append(ArgumentPair(emp, emp2, self.animation_box))

    def initiate_fight(self, emp, emp2):
        emp.in_interaction = True
        emp2.in_interaction = True
        emp.block_move = True
        emp2.block_move = True
        self.fight_pairs.append(FightPair(emp, emp2, self.animation_box))

# This class holds memonry of:
# - employees taking part of convo
# - all 3 topics that will be discussed (speech bubbles and the topic number)
# - whether employees agree or not about each of 3 topics
# - a timestamp for when the convo started
class ConversationPair:
    def __init__(self, emp1: Employee, emp2: Employee, animation_box: dict):
        self.emp1 = emp1
        self.emp2 = emp2
        self._topic_index = 0
        self.topic_list = self.init_topics(emp1, emp2)
        self._MAX_TOPICS = 2
        self.emps_agree_on_topic_list = self.calculate_conversation_result(emp1, emp2, self.topic_list)
        self.speech_bubble_animation_list = [animation_box.get("speech_bubbles")[topic_number] for topic_number in
                                             self.topic_list]
        self.disagree_bubble = animation_box.get("speech_bubbles")[DISAGREE_SPEECH_BUBBLE_INDEX]
        self.start_topic_speech_bubble_triggered = False
        self.response_speech_bubble_triggered = False
        self.conversation_timestamp = time.get_ticks()

    def calculate_conversation_result(self, emp1, emp2: Employee, topics_list):
        return [self.calculate_topic_result(emp2, topics_list[0]),
                self.calculate_topic_result(emp1, topics_list[1]),
                self.calculate_topic_result(emp2, topics_list[2])]

    def calculate_topic_result(self, convo_responder, topic_number):
        # if emp2 has 2 out of 5 in interest scale
        # then emp2 has 2/5 chance to like the topic
        # -1 means they disagree
        conversation_result = -1

        convo_responder_topic_dice = random.randrange(1, convo_responder.interests.MAX_INTEREST + 1)
        if self._is_convo_responder_interested_in_topic(topic_number, convo_responder_topic_dice,
                                                        convo_responder):
            return 1
        return conversation_result

    def _is_convo_responder_interested_in_topic(self, topic_number, responder_topic_dice, convo_responder):
        return responder_topic_dice <= convo_responder.interests.interests_list[topic_number]

    # this way emp2 can start conversation and emp1 respond
    def swap_conversation_roles(self):
        mem = self.emp1
        self.emp1 = self.emp2
        self.emp2 = mem

    # get the top 2 interesting topics from emp1
    # and top 1 topic from emp2
    def init_topics(self, emp1: Employee, emp2: Employee):
        topic_list = []
        interests_list = emp1.interests.interests_list.copy()
        # index of the maximum interest value in the interest list
        # basically means get the topic index of the most interesting topic for the employee
        interesting_topic = interests_list.index(max(interests_list))
        topic_list.append(interesting_topic)
        interests_list.pop(interesting_topic)

        topic_list.append(emp2.interests.interests_list.index(max(emp2.interests.interests_list)))

        topic_list.append(interests_list.index(max(interests_list)))
        return topic_list

    def trigger_current_start_topic_speech_bubble_once(self):
        if not self.start_topic_speech_bubble_triggered:
            self.speech_bubble_animation_list[self._topic_index].trigger()
            self.start_topic_speech_bubble_triggered = True

    def attach_current_start_topic_speech_bubble_to_emp(self):
        self.speech_bubble_animation_list[self._topic_index].rect.x = self.emp1.rect.x + 20
        self.speech_bubble_animation_list[self._topic_index].rect.y = self.emp1.rect.y - 30

    def attach_current_respond_speech_bubble_to_emp(self):
        self.speech_bubble_animation_list[self._topic_index].rect.x = self.emp2.rect.x + 20
        self.speech_bubble_animation_list[self._topic_index].rect.y = self.emp2.rect.y - 30
        self.disagree_bubble.rect.x = self.emp2.rect.x + 20
        self.disagree_bubble.rect.y = self.emp2.rect.y - 30

    def trigger_current_respond_speech_bubble_once(self):
        if not self.response_speech_bubble_triggered:
            if self.emps_agree_in_topic(self._topic_index):
                self.speech_bubble_animation_list[self._topic_index].trigger()
            else:
                self.disagree_bubble.trigger()
            self.response_speech_bubble_triggered = True

    def emps_agree_in_topic(self, topic_index):
        return self.emps_agree_on_topic_list[topic_index] == 1

    def next_topic(self):
        self._topic_index += 1
        self.conversation_timestamp = time.get_ticks()

    def is_last_topic(self):
        return self._topic_index == self._MAX_TOPICS

    def finish_topic(self):
        self.response_speech_bubble_triggered = False
        self.start_topic_speech_bubble_triggered = False

    def unblock_movement(self):
        self.emp1.block_move = False
        self.emp2.block_move = False


# This pair will always produce negative relation of value self.relation_penalty
# An argument bubble appears during the argument
class ArgumentPair:
    def __init__(self, emp1: Employee, emp2: Employee, animation_box):
        self.emp1 = emp1
        self.emp2 = emp2
        self.relation_penalty = -3
        self.argument_timestamp = time.get_ticks()
        self.start_argument_bubble_triggered = False
        self.response_argument_bubble_triggered = False
        self.argument_bubble_animation = animation_box.get("argument_bubble")

    def trigger_current_start_argument_bubble_once(self):
        if not self.start_argument_bubble_triggered:
            self.argument_bubble_animation.trigger()
            self.start_argument_bubble_triggered = True

    def attach_current_start_argument_bubble_to_emp(self):
        self.argument_bubble_animation.rect.x = self.emp1.rect.x + 20
        self.argument_bubble_animation.rect.y = self.emp1.rect.y - 30

    def attach_current_respond_argument_bubble_to_emp(self):
        self.argument_bubble_animation.rect.x = self.emp2.rect.x + 20
        self.argument_bubble_animation.rect.y = self.emp2.rect.y - 30

    def trigger_current_respond_argument_bubble_once(self):
        if not self.response_argument_bubble_triggered:
            self.argument_bubble_animation.trigger()
            self.response_argument_bubble_triggered = True

    def finish_argument(self):
        self.response_argument_bubble_triggered = False
        self.start_argument_bubble_triggered = False

    def unblock_movement(self):
        self.emp1.block_move = False
        self.emp2.block_move = False


class FightPair:
    def __init__(self, emp1: Employee, emp2: Employee, animation_box):
        self.emp1 = emp1
        self.emp2 = emp2
        self.emp1_image = self.emp1.image
        self.emp2_image = self.emp2.image
        self.relation_penalty = -5
        self.fight_timestamp = time.get_ticks()
        self.fight_animation_triggered = False
        self.fight_animation = animation_box.get("fight_cloud")

    def trigger_fight_animation_once(self):
        if not self.fight_animation_triggered:
            self.fight_animation.trigger()
            self.fight_animation_triggered = True
            self.emp1_image = self.emp1.image
            self.emp2_image = self.emp2.image

    def attach_fight_cloud_to_emp(self):
        self.fight_animation.rect.x = (self.emp1.rect.x + self.emp2.rect.x) / 2
        self.fight_animation.rect.y = self.emp1.rect.y + 10
        self.emp1.sitting_sprite_disappear()
        self.emp2.sitting_sprite_disappear()


    def finish_fight(self):
        if self.fight_animation_triggered:
            self.fight_animation_triggered = False
            self.emp1.image = self.emp1_image
            self.emp2.image = self.emp2_image

    def unblock_movement(self):
        self.emp1.block_move = False
        self.emp2.block_move = False

