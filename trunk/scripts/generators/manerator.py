import random

def _getMan():
    bodyTypes = ['short','tall','squat','slim','fat','bulky','broad']

    hairLengths = ['short','long','no','curly','straight']

    hairFarbs = [' red',' black',' brown',' white',' blond']

    eyeFarbs = ['blue','brown','green','hazel','golden','red','dark','violet']

    attrs = ['intelligent','cheerful','hardworking','adventurous','wealthy','kind','calm','regal','mildly perturbed','suspicious','wild']

    bodSelect = random.choice(bodyTypes)
    hairSelect = random.choice(hairFarbs)
    hairLSel = random.choice(hairLengths)
    if hairLSel == "no":
        hairSelect = ""
    else:
        pass
    eyeSel = random.choice(eyeFarbs)
    feelType = random.choice(attrs)

    string = "A %s man with %s%s hair. His eyes are %s. His carriage seems %s." % (bodSelect,hairLSel,hairSelect,eyeSel,feelType)
    
    return string

def getName(args):
    return _getMan()