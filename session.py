import logging
from random import choice

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

with open('speech_assets/customSlotTypes/LIST_OF_ANSWERS') as f:
     answers = [a.strip() for a in f.readlines()]

# AMAZON.NoIntent | AMAZON.RepeatIntent | AMAZON.YesIntent

@ask.launch
def launch():
    card_title = render_template('card_title')
    question_text = render_template('welcome')
    reprompt_text = render_template('welcome_reprompt')
    return question(question_text).reprompt(reprompt_text).simple_card(card_title, question_text)


@ask.intent('AMAZON.NoIntent')
def no():
    no_text = render_template('no')
    return statement(no_text)

@ask.intent('AMAZON.YesIntent')
def yes():
    actual_answer = random.choice(answers)
    yes_text = render_template('yes', actual_answer=actual_answer)
    return question(yes_text)

@ask.intent('AnswerIntent', mapping={'answer': 'Answer'})
def my_answer_is(answer):
    card_title = render_template('card_title')

    if answer is not None:
        if answer == actual_answer:
            response_text = render_template('correct_response', actual_answer=answer)
            reprompt_text = render_template('welcome_reprompt')
            return statement(response_text).question(reprompt_text)
        else:
            response_text = render_template('incorrect_response', actual_answer=answer)
            reprompt_text = render_template('welcome_reprompt')
            return statement(response_text).question(reprompt_text)
    else:
        yes_text = render_template('yes', actual_answer=actual_answer)
        return question(yes_text)

@ask.intent('AnswerOnlyIntent', mapping={'answer': 'Answer'})
def only_answer_is(answer):
    card_title = render_template('card_title')

    if answer is not None:
        if answer == actual_answer:
            response_text = render_template('correct_response', actual_answer=answer)
            reprompt_text = render_template('welcome_reprompt')
            return statement(response_text).question(reprompt_text)
        else:
            response_text = render_template('incorrect_response', actual_answer=answer)
            reprompt_text = render_template('welcome_reprompt')
            return statement(response_text).question(reprompt_text)
    else:
        yes_text = render_template('yes', actual_answer=actual_answer)
        return question(yes_text)

# @ask.intent('WhatsMyColorIntent')
# def whats_my_color():
#     card_title = render_template('card_title')
#     color = session.attributes.get(COLOR_KEY)
#     if color is not None:
#         statement_text = render_template('known_color_bye', color=color)
#         return statement(statement_text).simple_card(card_title, statement_text)
#     else:
#         question_text = render_template('unknown_color_reprompt')
#         return question(question_text).reprompt(question_text).simple_card(card_title, question_text)



@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
