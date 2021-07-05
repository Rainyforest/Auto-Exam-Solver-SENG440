from solvers import *

p3 = StandardPeripheralsCountersSolver(
    f_osc=100,
    divider = 1,
    counter_base = 10,
    counter_digits = 6)

p4 = StandardPeripheralsADConversionSolver(
    is_linear = False,
    is_pure_expansion = False,
    converter_bits = 13,
    pre_compression = 0.75,
    post_compression = 0.5
)

p5 = StandardPeripheralsUARTSolver(
    prob_dicts = {
        'a':0.25,
        'b':0.25,
        'c':0.5,
    },
)

p1 = SoftwareOptimizationTechniquesSolver(
    result = '''
register int i;
int summation( int *samples) {
    register int sum = 0;
    for( i=0; i < 128; i++) {
        sum += samples[i];
    }
    return sum;
}
    '''
)

p2 = FixedPointArithmeticSolver(
    
)

problems = [p1,p2,p3,p4,p5]

f = open("demo.txt", "a")
[f.write("\n============================\nProblem {}\n".format(i) + p.out())
    for i,p in enumerate(problems,1)]
f.close()