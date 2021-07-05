from solvers import *

p1 = StandardPeripheralsCountersSolver(
    f_osc=50,
    divider = 5,
    counter_base = 10,
    counter_digits = 5)

p2 = StandardPeripheralsADConversionSolver(
    is_linear = False,
    is_pure_expansion = False,
    converter_bits = 12,
    pre_compression = 0.75,
    post_compression = 0.5
)

p3 = StandardPeripheralsUARTSolver(
    prob_dicts = {
        'a':1/10,
        'b':1/10,
        'c':1/10,
        'd':1/10,
        'e':1/10,
        'f':1/10,
        'g':4/10,
    },
    baud = 19200
)

p4 = SoftwareOptimizationTechniquesSolver(
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

# p5 = FixedPointArithmeticSolver(

# )

problems = [p1,p2,p3,p4]

f = open("demo.txt", "a")
[f.write("\n============================\nProblem {}\n".format(i) + p.out())
    for i,p in enumerate(problems,1)]
f.close()