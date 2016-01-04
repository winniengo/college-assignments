#!/usr/bin/env python

import sys

def concordance(words, i, eval=None):
    if i-20 < 0:
        prechars = ' '.join(words[:i])[-30:]
    else:
        prechars = ' '.join(words[i-20:i])[-30:]
        
    center = words[i]

    if i+21 >= len(words):
        postchars = ' '.join(words[i+1:])[:30]
    else:
        postchars = ' '.join(words[i+1:i+21])[:30]
        
    if eval is not None:
        label = '[%s]' % (eval)
    else:
        label = ''
    print "%30s  %s  %-30s    %s" % (prechars, center, postchars, label)
    

def evaluate(guesses, truths, words, verbose=0):
    """
    verbose:
      0 = show nothing
      1 = show incorrect
      2 = show all
    """
    n = len(words)
    
    t = 0
    g = 0

    tp = 0
    fp = 0
    fn = 0
    while g < len(guesses) and t < len(truths):
        guess = guesses[g]
        if guess == truths[t]:
            if verbose == 2:
                concordance(words, guesses[g], 'TP')
            tp += 1
            t += 1
            g += 1
        elif guess < truths[t]:
            if verbose >= 1:
                concordance(words, guesses[g], 'FP')
            fp += 1
            g += 1
        elif guess > truths[t]:
            if verbose >= 1:
                concordance(words, truths[t], 'FN')
            t += 1
            fn += 1

    fn += (len(truths) - t)
    tn = n-tp-fp-fn
    return (tp, fp, fn, tn)



if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print "Usage: evaluate.py <category> <guesses> [verbose: 0,1,2]"
        print "  verbose = 0: show results summary"
        print "  verbose = 1: show concordance for FP, FN only"
        print "  verbose = 2: show concordance for TP, FP, FN only"
        sys.exit(-1)
    else:
        cat = sys.argv[1]
        guesses = sys.argv[2]
        if len(sys.argv) == 4:
            verbose = int(sys.argv[3])
        else:
            verbose = 0
        

    loc = '/data/cs65/misc/'
    
    words = [x.rstrip() for x in open('%s/%s.txt' % (loc, cat)).readlines()]
    eos = [int(x.rstrip()) for x in open('%s/%s-eos.txt' % \
                                         (loc, cat)).readlines()]
    if guesses == "-":
        fh = sys.stdin
    else:
        fh = open('%s' % (guesses))
        
    answers = [int(x.rstrip()) for x in fh.readlines()]

    (tp, fp, fn, tn) =  evaluate(answers, eos, words, verbose)
    if verbose == 0:
        print "TP: %7d\tFN: %7d" % (tp, fn)
        print "FP: %7d\tTN: %7d" % (fp, tn)
        prec = float(tp) / (tp+fp)
        recall = float(tp) / (tp+fn)
        f = 2*prec*recall/(prec+recall)
        print "PRECISION: %5.2f%%\tRECALL: %5.2f%%\tF: %5.2f" % \
              (prec*100, recall*100, f)
    
        

