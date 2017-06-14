# mathhammer
A python script for modelling warhammer 40k 8th edition damage probability

```Syntax:  mathhammer.py <num shots> <bs/ws> <s> <ap> <t> <sv> <d>```

To calculate 20 bolter shots from a space marine into other space marines:
```mathhammer.py 20 3+ 4 0 4 3+ 1```

The result is the following chart:
```
Damage   Outcomes        percent
     0       9489         9.5%
     1      23751        23.8%
     2      28360        28.4%
     3      20966        21.0%
     4      11213        11.2%
     5       4466         4.5%
     6       1339         1.3%
     7        338         0.3%
     8         68         0.1%
     9         10         0.0%
```

This chart means that, of all the hypothetical die rolls involved in trying these 20 attacks 100000 times, 28.4% of the time, 2 damage is dealt to the opposing squad of space marines.

The script is aware of damage and number of attacks.  Damage can be in integer values, or die notation (2d6, d6, d3, etc).  Ballistic skill and Saves can be expressed as integers or in 40k stat notation (3+, 2+, etc)

It is not capible of handling special rules such as rerolls at this time.
Future functionality may include providing invulnerable saves, but they are not implemented at this time.

Note that since this script uses psuedorandom data to generate its result, each execution with the same parameters may provide a different result.  

Also note that it depends on the secrets module's number generator, which is supposedly better than the random module.  I think it still depends on the underlying OS's RNG system, which is said to be lackluster in Windows.  I've not tested it on other OSs yet, though I can think no reasons why it wouldn't be compatible.
