#Random commit comment generator. By Doctus.
import random

verbs = ['added', 'improved', 'enhanced', 'fixed', 'repaired', 'removed', 'deleted', 'edited', 'modified', 'expanded', 'worked on']
adjs = ['helpful', 'assorted', 'various', 'several', 'GUI', 'network', 'backend', 'frontend', 'logic', 'processing', 'old']
nouns = ['bugs', 'features', 'routines', 'functions', 'signals', 'objects', 'classes', 'interfaces', 'widgets']

def getCommitComment():
  patterns = [[random.choice(verbs), random.choice(adjs), random.choice(nouns)],
            [random.choice(verbs), random.choice(nouns), "and", random.choice(verbs), random.choice(adjs),
             random.choice(nouns)],
            [random.choice(verbs), random.choice(adjs), random.choice(adjs), random.choice(nouns), "and",
             random.choice(verbs), random.choice(adjs), random.choice(nouns)],
              [random.choice(verbs), random.choice(adjs), random.choice(adjs), random.choice(nouns), "and mostly",
             random.choice(verbs), random.choice(adjs), random.choice(nouns)]]
  return (" ".join(random.choice(patterns))).capitalize() + "."

#for r in range(0, 10):
#  print getCommitComment()
print "\"" + getCommitComment() + "\""
