from sys import flags, float_info
import math
from typing import Text

class ProblemSolver:
    def __init__(self,  **kwargs):
        pass
    
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
        sum_of_bits = 0
        for k,v in self.prob_dicts.items():
            amount_of_bits = -math.log(v,2)
            text += "Amount of information for {k}: p_{k} = -log2(v) = {res:.3f}\n".format(k=k,v=v,res=amount_of_bits)
            sum_of_bits+=amount_of_bits
        if self.baud:
            bit_rate = sum_of_bits/3*self.baud
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
    

class Oprand():
    def __init__(self,name,value,sf) -> None:
        self.name = name
        self.value = value
        self.sf = sf

class FixedPointArithmeticSolver(ProblemSolver):
    def out(self):
        # c = FixedPointArithmeticSolver()
        # [outx,textx] = c.real_to_integer(
        #     var_name='x',
        #     real = 0.11,
        #     real_range=(-0.11,0.11),
        #     bits = 16
        # )
        # [outy,texty] = c.real_to_integer(
        #     var_name='y',
        #     real = -0.39,
        #     real_range=(-0.41,0.44),
        #     bits = 13
        # )
    
        # [outpdp,textm] = c.fractional_multiplier(outx,outy,29)
        # [outp,textr] = c.V_Neumann_rounding(outpdp,21)
        
        return ''
      
    # def cut_bits(self, decimal, bits):

    def real_to_integer(self, var_name, real, real_range, bits):
        # get scaling factor
        range_bound = max(abs(real_range[0]),abs(real_range[1]))
        bound_exp = math.ceil(math.log(range_bound,2))
        res_exp = bits - 1
        sf_exp = res_exp - bound_exp
        decimal = round(2**sf_exp*real)
        sign = 1 if real < 0 else 0
        binary = bin(decimal & (2**bits-1))[2:].zfill(bits)
        hexadecimal = hex(int(binary,2))
        large_var_name = var_name.capitalize()
        out = 0
        text = '''
Real to Integer
-----------------------------
Range of the real number {var_name}         : {real_range}
Bound in 2's power                 : (-2^{bound_exp}, 2^{bound_exp})
Required bits (remove sign bit)    : (-2^{res_exp}, 2^{res_exp})
Scaling factor                     : 2^{sf_exp}
{large_var_name} = round(2^{sf_exp}*{real}) = {decimal} = ({binary})b = ({hexadecimal})h
        '''.format(var_name = var_name,
                    real_range=real_range,
                    bound_exp=bound_exp,
                    res_exp=res_exp,
                    sf_exp = sf_exp,
                    large_var_name = large_var_name,
                    real=real,
                    decimal=decimal,
                    binary=binary,
                    hexadecimal = hexadecimal
                    )
        return [Oprand(large_var_name,decimal,sf_exp),text]
    
    def fractional_multiplier(self,op1,op2,bits): #Pdp
        factor = (bits-1)-(op1.sf+op2.sf)
        pdp = 2**(factor)*op1.value*op2.value
        binary = bin(int(pdp) & (2**bits-1))[2:].zfill(bits)
        hexadecimal = hex(int(binary,2))
        text = '''
Fractional Multiplier
-----------------------------
{X}*{Y} = {X}/(sf{X}) * {Y}/(sf{Y}) = {X}{Y} * 2^factor / 2^{bits}
We can get factor = {bits} - 1 - （sf{X} + sf{Y}）= {factor}
By multiplying {X},{Y},2^{factor} and then mask with the required number of bits,
we get {X}*{Y} = {pdp} = ({binary})b = ({hexadecimal})h
        '''.format(
            X=op1.name,
            Y=op2.name,
            bits=bits,
            factor=factor,
            pdp=pdp,
            binary=binary,
            hexadecimal = hexadecimal
        )
        return [Oprand("Pdp",pdp,op1.sf+op2.sf+1),text]

    def integer_multiplier(self,op1,op2,bits): #Pdp
        pdp = op1.value*op2.value
        binary = bin(pdp & (2**bits-1))[2:]
        sign = '1' if pdp<0 else '0'
        # filling
        binary = sign*(bits-len(binary))+binary if len(binary)<bits else binary
        hexadecimal = hex(int(binary,2))
        text = '''
Integer Multiplier
-----------------------------
{X}*{Y} = {X}/(sf{X}) * {Y}/(sf{Y}) = {X}{Y} / 2^{bits}
By multiplying {X},{Y} and mask with the required number of bits,
we get {X}*{Y} = {pdp} = ({binary})b = ({hexadecimal})h
        '''.format(
            X=op1.name,
            Y=op2.name,
            bits=bits,
            pdp=pdp,
            binary=binary,
            hexadecimal = hexadecimal
        )
        return [Oprand("Pdp",pdp,op1.sf+op2.sf),text]

    def V_Neumann_rounding(self, op, bits):
        shift_bits = op.sf - bits
        value = op.value
        flag = int(op.value) & 2**(shift_bits)-1 > 0
        is_need = '' if flag else "don't "
        value = int(value) >> shift_bits 
        if flag: value = value | 1
        binary = bin(value & (2**bits-1))[2:].zfill(bits)
        hexadecimal = hex(int(binary,2))
        text = '''
V_Neumann_rounding  
-----------------------------
We shift {name} to round it to {bits}
{opbits} - {bits} = {shift_bits} need to be shifted,
also before shifting we check if they have any one in it
it turns out we {is_need}need to set the least significant bit 1.
The output is finally {value} = ({binary})b = ({hexadecimal})h.
        '''.format(
            name=op.name,
            bits=bits,
            opbits=op.sf,
            shift_bits=shift_bits,
            is_need=is_need,
            value=value,
            binary=binary,
            hexadecimal=hexadecimal
        )
        return [Oprand("P",value,op.sf-shift_bits), text]

    def truncate(self, op, bits):
        shift_bits = op.sf - bits
        value = op.value
        value = value >> shift_bits 
        binary = bin(value & (2**bits-1))[2:].zfill(bits)
        hexadecimal = hex(int(binary,2))
        text = '''
Truncate  
-----------------------------
We shift {name} to round it to {bits}
{opbits} - {bits} = {shift_bits} need to be shifted,
also before shifting we check if they have any one in it
The output is finally {value} = ({binary})b = ({hexadecimal})h.
        '''.format(
            name=op.name,
            bits=bits,
            opbits=op.sf,
            shift_bits=shift_bits,
            value=value,
            binary=binary,
            hexadecimal=hexadecimal
        )
        return [Oprand("R",value,op.sf-shift_bits), text]

    def absolute(self, op, bits):
        decimal = ~op.value + 1
        binary = bin(decimal & (2**bits-1))[2:].zfill(bits)
        hexadecimal = hex(int(binary,2))
        text = '''
Absolute {name}
-----------------------------
Get absolute value of {name}, the result is ({binary})b = ({hexadecimal})h.
        '''.format(
            name=op.name,
            binary=binary,
            hexadecimal=hexadecimal
        )
        return [Oprand("ABS({})".format(op.name),decimal,bits), text]

    def add(self, op1, op2, bits):
        decimal = op1.value + op2.value
        print(op1.sf)
        print(op2.sf)
        binary = bin(decimal & (2**bits-1))[2:].zfill(bits)
        hexadecimal = hex(int(binary,2))
        text = '''
Add
-----------------------------
Get the sum of value {name1} and {name2}, the result is ({binary})b = ({hexadecimal})h.
        '''.format(
            name1=op1.name,
            name2=op2.name,
            binary=binary,
            hexadecimal=hexadecimal
        )
        return [Oprand("SUM",decimal,bits),text]
        
def main():
    c = FixedPointArithmeticSolver()
    [outx,textx] = c.real_to_integer(
        var_name='x',
        real = 0.11,
        real_range=(-0.11,0.11),
        bits = 16
    )
    [outy,texty] = c.real_to_integer(
        var_name='y',
        real = -0.39,
        real_range=(-0.41,0.44),
        bits = 13
    )

    [outpdp,textm] = c.fractional_multiplier(outx,outy,29)
    [outp,textr] = c.V_Neumann_rounding(outpdp,21)
    print(textx)
    print(texty)
    print(textm)
    print(textr)

if __name__ == "__main__":
    main()
