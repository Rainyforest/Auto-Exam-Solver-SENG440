from sys import float_info
import math

class ProblemSolver:
    def __init__(self,  **kwargs):
        pass

    # Output latex paragraph for the problem
    def output():
        return ""

class SoftwareOptimizationTechniquesSolver(ProblemSolver):
    def __init__(self, **kwargs):
        self.result = kwargs.get('result')
    def out(self):
        return self.result

class StandardPeripheralsUARTSolver(ProblemSolver):
    def __init__(self, **kwargs):
        self.prob_dicts = kwargs.get('prob_dicts')
        self.baud = kwargs.get('baud')
    
    def out(self):
        text = ''''''
        amount_of_bits = 0
        for k,v in self.prob_dicts.items():
            amount_of_bits = -math.log(v,2)
            text += "Amount of information for {k}: p_{k} = -log2(v) = {res:.3f}\n".format(k=k,v=v,res=amount_of_bits)
        if self.baud:
            bit_rate = amount_of_bits*self.baud
            text += "Bit rate = baud * amount of bits = {bit_rate:.3f} bits/sec\n".format(bit_rate=bit_rate)
            text += "Byte rate = bit rate / 8 = {byte_rate:.3f} bits/sec\n".format(byte_rate=bit_rate/8)
        return text

class StandardPeripheralsADConversionSolver(ProblemSolver):
    def __init__(self, **kwargs):
        self.is_linear = kwargs.get('is_linear')
        self.is_pure_expansion = kwargs.get('is_pure_expansion')
        self.converter_bits = kwargs.get('converter_bits')
        # self.adc_func = kwargs.get('adc_func')
        self.pre_compression = kwargs.get('pre_compression')
        self.post_compression = kwargs.get('post_compression')

    def out(self):
        loss_in_accuracy = math.log(self.pre_compression,2)-math.log(self.post_compression,2)
        bits_to_trust = self.converter_bits - math.ceil(abs(loss_in_accuracy))
        linear_desc = '''
the conversion function is non-linear, thus we need to find a point where the real curve and ideal line have largest difference.
If the function is regular like quadratic, we could take a derivative   
        ''' 
        linear_desc = linear_desc if not self.is_linear else ""
        type = "expansion" if self.is_pure_expansion else "compression"
        text = '''
As we can observe, 
{linear_desc} 
The value before {type} is {pre_compression}
The value after {type} is {post_compression}

We calculate the loss in accuracy by:
    loss = log2({pre_compression}) - (log2({post_compression})) = {loss_in_accuracy:.3f}

Considering other potential error as well,
It is safe to trust {bits_to_trust} bits
        '''.format(linear_desc=linear_desc,
                    type=type,
                    pre_compression = self.pre_compression,
                    post_compression = self.post_compression,
                    loss_in_accuracy = loss_in_accuracy,
                    bits_to_trust = bits_to_trust
        )
        return text

class StandardPeripheralsCountersSolver(ProblemSolver):
    def __init__(self, **kwargs):
        self.f_osc = kwargs.get('f_osc')
        self.divider = kwargs.get('divider')
        self.counter_base = kwargs.get('counter_base')
        self.counter_digits = kwargs.get('counter_digits') 

    def out(self):
        f_clk = self.f_osc / self.divider
        t_clk = 1 / f_clk
        t_min = 2 * t_clk
        counter_max = self.counter_base ** self.counter_digits - 1;
        t_max = counter_max * t_clk
        f_max = 1 / t_min
        f_min = 1 / t_max
        f_max_accuracy = [1/(t_min+t_clk)-f_max, 1/(t_min-t_clk)-f_max]
        f_min_accuracy = [1/(t_max+t_clk)-f_min, 1/(t_max-t_clk)-f_min]
        is_f_max_Hz = False
        is_f_min_Hz = False
        if not all(abs(x) > 0.001 for x in f_max_accuracy):
            is_f_max_Hz = True
            f_max_accuracy = [10**6*x for x in f_max_accuracy]
        if not all(abs(x) > 0.001 for x in f_min_accuracy):
            is_f_min_Hz = True
            f_min_accuracy = [10**6*x for x in f_min_accuracy]

        def to_str_with_unit(x):
            if abs(x) < 0.001:
                return "{:.3f}".format((10**6)*x)+"Hz"
            return str(x)+"MHz"
            
        def getUnit(flag):
            if flag:
                return "Hz"
            return "MHz"

        text = '''
From the problem we can get:
clock frequency f_clk = f_osc / divider = {f_clk}MHz
clock period    t_clk = 1 / f_clk = {t_clk}

Max Frequency
Due to the intrinsic error, minimum period should be more than 1 clock period
Therefore t_min = 2 * t_clk = {t_min}
f_max = 1 / t_min = {f_max}

Accuracy
The counter recording periods has ±1 bit error,
Max frequency accuracy range: ( 1 / (t_min + t_ck), 1 / (t_min - t_ck))
The final result is {f_max} error:({f_max_accuracy_left:.3f},{f_max_accuracy_right:.3f}){e_max_unit}

Min Frequency
Due to the intrinsic error, maximum period should be as large as the counter could handle
Therefore t_max = counter_max * t_clk = {counter_max} * {t_clk} = {t_max}
f_min = 1 / t_max = {f_min}

Accuracy
The counter recording periods has ±1 bit error,
Max frequency accuracy range: ( 1 / (t_max + t_ck), 1 / (t_max - t_ck))
The final result is {f_min} error:({f_min_accuracy_left:.3f},{f_min_accuracy_right:.3f}){e_min_unit}
                '''.format(f_clk=f_clk,
                            t_clk=t_clk,
                            t_min=t_min,
                            f_max=to_str_with_unit(f_max),
                            f_max_accuracy_left=f_max_accuracy[0],
                            f_max_accuracy_right=f_max_accuracy[1],
                            e_max_unit=getUnit(is_f_max_Hz),
                            counter_max = counter_max,
                            t_max = t_max,
                            f_min = to_str_with_unit(f_min),
                            f_min_accuracy_left=f_min_accuracy[0],
                            f_min_accuracy_right=f_min_accuracy[1],
                            e_min_unit =getUnit(is_f_min_Hz) )
        return text
    



class FixedPointArithmeticSolver(ProblemSolver):
    pass

