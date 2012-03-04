import random

def _generateAdvice():
    anto = [['+cold', '+heat'], ['wisdom', '+fool'], ['+light', '+darkness'],
          ['victory', 'defeat'], ['evil', 'good'], ['sound', 'silence']]
    phrases = ["To find +~#, you must look within +@%.",
             "The greatest ~# is in the middle of +@%.",
             "The path of ~# leads to @%.",
             "Be wary of the ~# that cloaks itself as @%.",
             "When you see ~#, @% lies just above."]
    advice = random.choice(phrases)
    subject = random.choice(anto)
    if random.choice([True, False]): subject.reverse()
    advice = advice.replace("~#", subject[0])
    advice = advice.replace("@%", subject[1])
    advice = advice.replace('++', 'the ')
    advice = advice.replace('+', '')
    advice = advice.capitalize()
    return advice
  
def getName(args):
    return _generateAdvice()
