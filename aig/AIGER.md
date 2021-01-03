[TOC]

#AIGER
## 1. 介绍
AIGER是AIG()And-Inverter Graphs)的文件格式的代称，是瑞士境内阿尔卑斯山的一座山峰。AIGER格式CAV2007模型检测竞赛提供了一种简洁明了的文件格式。    
AIGER文件格式含有ASCII格式和二进制格式两个版本。当一个应用没有使用AIGER库时，可以生成ASCII格式的AIG文件。    
二进制格式更加简洁，格式更严谨，是基准测试和竞赛所采取的格式。生成二进制格式AIG文件有两种方法，第一种是用AIGER库直接生成，第二种是使用aigtoaig工具将ASCII格式转换成二进制格式(反过来也行，因此也将此工具用来验证二进制格式AIG文件的正确性)。   
在[http://fmv.jku.at/aiger/](http://fmv.jku.at/aiger/) 任意下载一个版本[aiger-1.9.1.tar.gz](fmv.jku.at/aiger/aiger-1.9.1.tar.gz), 在其中的`examples`目录下可以找到示例文件。      
>ASCII格式的AIG文件第一行由字符串`aag` 开始，`aag`是`ASCII AIG`的缩写；然后是以空格分隔5个非负整数，分别由`M, I, L, O, A` 表示。     
   
其中   
- `M` = 最大变量下标 maximum variable index
- `I` = 输入个数 number of inputs
- `L` = 锁存器个数 number of latches
- `O` = 输出个数 number of outputs
- `A` = 与门个数 number of AND gates
    
> 没有输入且没有输出的空电路AIG文件只包含如下的一行(`header`是注释)：  
```
aag 0 0 0 0 0 				header
```
> 包含如下两行的AIG文件代表常量`FALSE` ,其中`header`(第一行)中的1代表输出的个数为1，第二行代表唯一的输出`literal`.
```
aag 0 0 0 1 0				header
0							output
```
> 如下AIG文件代表常量`TRUE`
```
aag 0 0 0 1 0				header
1							output
```
> 下述文件是一个`buffer`， 第一行中，其中第一个数1为最大变量下标(`maximal variable index`)，第二个数1代表输入个数；第二行是一个输入`literal`(一个变量通过乘以2可以转换为文字`literal`，即如果输入为2的倍数且大于0，则它为一个`literal`)。在 第一种情况下，最后一行指定的输出和输入相同；在第二种情况下输出和输入相反，因为输出的文字`3`带有符号位(`3`的二进制表示的最低有效位为1，代表相反)
```
aag 1 1 0 1 0				header
2							input
2							output
```
>下列文件是一个`inverter` 
```
aag 1 1 0 1 0				header
2							input
3							output
```
>如下AIG文件表示一个与门(`AND gate`)。其中，第一行中的第一个数为3，代表最大变量下标(下标从0开始，即有`0,1,2,3`)；代表与门的文字为`6`，下标(从上至下来)为`3`；与门个数为1(第一行最后的数字)
```
aag 3 2 0 1 1
2               input 0
4               input 1
6               output 0
6 2 4           AND gate 0      1&2
```
>或门可以表示为
```
aag 3 2 0 1 1
2               input 0
4               input 1
7               output 0        !(!1&!2)
6 3 5           AND gate 0      !1&!2
```
>一个完整的组合电路。其中，symbol行是可选的(用来表示输入、锁存器、输出的符号)
```
aag 7 2 0 2 3               header line
2                           input 0         1st addend bit 'x'
4                           input 1         2nd addend bit 'y'
6                           output 0        sum bit        's'
12                          output 1        carry          'c'
6 13 15                     AND gate 0      x ^ y
12 2 4                      AND gate 1      x & y
14 3 5                      AND gate 2      !x & !y
i0 x                        symbol
i1 y                        symbol
o0 s                        symbol
o1 c                        symbol
c                           comment header
half adder                  comment
```
>时序电路使用锁存器(`latches`)作为状态变量，下述AIG文件是一个振荡转换电路，只含有一个锁存器和两个输出，没有输入；该系统包含两个相反的状态。
```
aag 1 0 1 2 0
2 3                         latch 0 with next state literal
2                           output 0
3                           output 1
```
>锁存器通常被初始化为0。下面使用了“使能信号”`enable`和额外的低电平复位信号作为输入，实现了上述振荡电路
```
aag 7 2 1 2 4
2                           input 0         'enable'
4                           input 1         'reset'
6 8                         latch 0         Q next(Q)
6                           output 0        Q
7                           output 1        !Q
8 4 10                      AND gate 0      reset & (enable ^ Q)
10 13 15                    AND gate 1      enable ^ Q
12 2 6                      AND gate 2      enable & Q
14 3 7                      AND gate 3      !enable & !Q
```
文字的顺序和与门的定义是无关的。二进制格式对顺序增加了更多的限制，也不允许出现未使用的文字。
## 2.设计选择
- 能对组合电路进行建模
- 能描述结构化的SAT问题
- 能对时序电路进行建模
- 能描述模型检测问题
- 操作符仅限于比特级别
- 操作符集合尽可能简单
- 具有简洁且标准化的二进制格式
- 应用程序能够方便地生成ASCII格式的AIG文件
- 应用程序能够方便读取二进制格式的AIG文件
- 具有符号表和注释
- 读取文件时能够按序舍弃符号表和注释
- 能够允许一些简单的拓展

## 3. ASCII格式
* ASCII格式的AIG文件在第一行(`header`行)具有一个格式标识符`aag`(是`ASCII AIG`的简写)，且文件的扩展名为`.aag`。    
AIGER库能够读取使用GNU GZIP压缩的包含AIG文件的压缩文件(压缩包需要具有`.gz`的扩展名)   
* `header`行后面紧接着的是`I`个输入，每行一个输入，均为非否定的文字(`literal`)，用正偶数来表示。
* 接下来是定义`L`个锁存器，每行一个。每一个锁存器定义都由两个正整数表示，第一个正整数是偶数，表示该锁存器当前状态；第二个用来指示该锁存器的下个状态。
* 然后是`O`个输出文字(`output literals`)，每行一个。输出文字的内容是任意的。
* 之后是`A`个与门的定义，每行一个。每一个与门包含3个正整数，相邻整数用一个空格分开。第一个整数是偶数，表示与门的左值(`left-hand side, LHS`,结果)；其余两个整数表示与门的右值(`right-hand side, RHS`，输入)
* 为了保持结构良好，`I`个输入文字需要彼此不相同，`L`个锁存器的当前状态文字也互不相同，以及`A`个与门的左值`LHS`文字互不相同，因此恰好需要`I+L+A`个文字。
* 其他没定义的文字，除了两个常量`0`和`1`外，均不能用来作为输出文字，也不能作为下个状态文字，也不能作为与门的右值`RHS`文字。
* 与门的定义必须不能循环依赖，即某与门的左值LHS文字不能和同一与门的右值RHS文字相同(在去掉符号位的情况下)。这种依赖关系的传递非自反闭包必须是无环的。
* ASCII格式的AIG文件需要先检查无定义的文字和循环依赖，而格式约束较多的二进制格式则不需要进行检查。AIGER库中的`aignm`和`aigtoaig`均可以用来检查AIG文件的格式是否正确。
* 最后一点，ASCII格式的AIG文件中定义的文字个数不一定要和最大变量下标`M`相等，因为有些文字可能不需要用到。

## 4. 符号表(Symbols table)
在定义了与门之后，可以选择定义一个符号表(Symbols table)。一个符号是一个可打印字符(除去换行符)所组成的字符串。符号只能被赋予输入、锁存器和输出，且每个输入、锁存器和输出只能被分别赋予一个符号。一个符号占据一行。符号类型指示符由`i,l,o`加上一个位置(在输入、锁存器、输出中的位置，例如该符号指示第一个输入，则其位置为0)组成，符号名称是一个字符串，符号表中的一项则由符号类型指示符合符号名称构成，结构如下：
```
[ilo]<pos> <string>
```
符号表和注释放置在各种定义之后，所以应用程序读取AIG文件则只需读取定义后就停止读取。

## 5. 注释(comment)
可选的注释内容放置在文件最后。注释部分有一个注释头(`comment header`)，该注释头由一个单独的字符`c`开始，最后是一个换行符。注释头下面的每一行都是注释。如果有注释，则文件的最后一个字符必须为换行符。

## 6. 二进制格式的优势
二进制格式比ASCII格式更加严格。文字必须按照特定的顺序排列。顺序限制和数字的二进制补码表示能够使得二进制格式文件更加易于阅读且更加简洁。实验表明，这些限制和额外的增量编码能够构造更小的文件。某模型的二进制格式文件通常比经过GZIP压缩的ASCII格式的文件更小。压缩二进制格式能够得到更小容量的文件。

## 7.二进制格式的定义
在语义上，二进制格式是ASCII格式的一个子集，只在语法上有些不同。将一个二进制格式文件转换为一个ASCII格式文件，再转换回二进制格式，会得到与转换之前相同的二进制格式文件，即便二进制格式会重新编码文字(`reencode literals`)。   
如果定义了输入文字，则所有锁存器的当前状态文字可以省略。   
与门的定义是二进制编码的。   
符号表和注释部分的定义和ASCII格式文件相同。   
二进制格式文件(`.aig`文件)的`header`是使用ASCII格式。示例如下：
```
aig M I L O A
```

<br>

常量、变量和文字的处理方式和ASCII格式的AIG文件一样。   
二进制文件在输入变量、锁存器、与门的变量下标和定义位置上做出了限制。    
首先定义输入变量的下标，接着是定义锁存器的`pseudo-primary input`(伪初始输入)的下标，   
最后是定义与门的左值(LHS)文字的下标
```
input variable indices        1,          2,  ... ,  I
latch variable indices      I+1,        I+2,  ... ,  (I+L)
AND variable indices      I+L+1,      I+L+2,  ... ,  (I+L+A) == M
```
与上面对应的无符号文字分别是
```
input literals                2,          4,  ... ,  2*I
latch literals            2*I+2,      2*I+4,  ... ,  2*(I+L)
AND literals          2*(I+L)+2,  2*(I+L)+4,  ... ,  2*(I+L+A) == 2*M
```
所有文字必须被定义，因此必须严格满足等式`M=I+L+A`。有了这条限制，我们可以省略锁存器的当前状态文字。   
因此，在`header`行之后，紧接着是`L`个下一状态文字，每行一个，分别代表一个锁存器。   
然后是`O`个输出文字，也是每行一个。

<br>

在二进制格式中，与门的排列是有序的，遵循父子关系。与门的左值文字比较小的排列在前面。   
一个与门的右值文字都要比它的左值文字要小。   
我们可以将一个与门的右值文字排序，将较大的文字排在前面。例如下面的与门定义：
```
lhs rhs0 rhs1
```
其中`lhs`是偶数，并且`lhs>rhs0>=rhs1`。  
为了防止组合逻辑自循环(`combinational self loops`)，变量下标被设置成两两不同   
因为所有与门的左值(LHS)文字是连续的(偶数)，所以在二进制格式的文件中，我们不需要保存`LHS`。   
根据上述描述，我们可以只用`delta0`和`delta1`表示一个与门(binary delta encoding,二进制增量编码)，其中：
```
delta0 = lhs-rhs0, delta1 = rhs0-rhs1
```
这两者都不会是负数，且数值比较小，当使用简单的小端编码时会有优势。   
定义完与门之后，便是可选的符号表和注释部分(和ASCII格式一样)

## 8.二进制增量编码
假设`w0,...,wi`都是7位比特的文字，`w1,..wi`均不为0，且无符号整数`x`能够表示为
```
x = w0 + 2^7*w1 + 2^14*w2 + 2^(7*i)*wi
```
则`x`在AIGER格式中可以用二进制编码为`i`个字节序列`b0,b1,b2,...,bi`：
```
b0,b1,b2,...,bi = 1w0, 1w1, 1w2, ..., 0wi
```
序列中每个字节的最高有效位(`MSB`)用来指示该字节是否为此序列的最后一个字节。示例如下：
```
    unsigned integer   byte sequence of encoding (in hexadecimal)
 
                     x   b0 b1 b2 b3
                        
                     0   00
                     1   01
      2^7-1    =   127   7f
      2^7      =   128   80 01
      2^8  + 2 =   258   82 02
      2^14 - 1 = 16383   ff 7f
      2^14 + 3 = 16387   83 80 01
      2^28 - 1           ff ff ff 7f
      2^28 + 7           87 80 80 80 01
```
这种编码最多可以减少4倍的字节数，特别是文件中的含有大量数值较小的整数时。
这种对任意精度无符号整数的二进制编码与平台无关，因此是64位机器完全支持。
以下C代码可以用来表明这种编码-解码方法非常方便，但该方法无法运行，其中存在栈溢出和文件错误。
```
    unsigned char
    getnoneofch (FILE * file)
    {
      int ch = getc (file);
      if (ch != EOF)
        return ch;

      fprintf (stderr, "*** decode: unexpected EOF\n");
      exit (1);
    }

    unsigned
    decode (FILE * file)
    {
      unsigned x = 0, i = 0;
      unsigned char ch;

      while ((ch = getnoneofch (file)) & 0x80)
        x |= (ch & 0x7f) << (7 * i++);

      return x | (ch << (7 * i));
    }

    void
    encode (FILE * file, unsigned x)
    {
      unsigned char ch;

      while (x & ~0x7f)
        {
          ch = (x & 0x7f) | 0x80;
          putc (ch, file);
          x >>= 7;
        }
     
      ch = x;
      putc (ch, file);
    }
```
不检查读取的字符是否为EOF可能会导致无限循环。在AIG文件的二进制格式中，读取上述的二进制编码序列需要一次性读完，如果没有读完序列就遇到了EOF，则会发生解析错误。解决方法是检查`getc`返回的字符，若是EOF，则终止解析。


## 9. 性质检测(property checking)
AIGER格式可以方便地用于各种类型的性质检测。   
我们可以强制一个不包含锁存器、且只含一个输出的组合逻辑电路输出为1，这是对SAT问题的编码。   
验证时序逻辑电路上的安全性质的模型检测问题也可以进行同样的编码。  
若是为了验证`liveness`，我们可以将每个输出解释为公平约束。   
一种能够找出给定公平约束所对应的一个可达公平循环(`reachable fair cycle`)的算法可以用来对LTL性质进行模型检测。   
接下来我们计划使AIG文件能够支持PSL性质的描述。   
当前仅允许电路输出作为原子特性。   
可以通过引用符号表中所定义的符号名来引用输出文字。

## 10. Vectors, Stimulus, Traces, Solutions and Witnesses
此节给出了性质检测问题中的`traces`和`solutions`的语义和语法。   
具体而言，此节只考虑结构化SAT求解问题和坏态检测问题。   
本质上，一个有效的`solution`是一个输入向量(vector)组成的列表(list)。输入向量包含三种值`0,1,x`。该`solution`是一个有效的`witness`，当且仅当将`x`用`0`或者`1`实例化之后，AIG文件的二值模拟能够输出至少一个`1`(假设AIG文件是从全为`0`的初始状态出发的)。   
对于结构化SAT求解问题，AIG文件中不包含锁存器，这种情况下只需一个输出就足够了。
原则上，在部分二值输入已赋值的情况下，可以用三值逻辑来模拟AIG文件。  
三值逻辑中使用到了`0,1,x`，三值逻辑的逻辑操作如下：
```
a !a     & 0 1 x
0  1     0 0 0 0
1  0     1 0 1 x
x  x     x 0 x x
```
一个大小为n的值向量(`vector of values`)是一个具有n个三值常量的列表，使用长度为n的ASCII码字符串表示，每个字符可以为`0`， `1`或者`x`。
给定一个AIG文件的，其类型表示为`M I L O A`。它对应的一个输入向量大小为`I`，输出向量大小为`O`，状态向量大小为`L`。   
AIG文件的一个`stimulus`是一个输入向量的列表。一个`stimulus`对应的文件是一个多行ASCII字符串，每一行字符串用一个换行符分隔，文件末尾使用一个换行符结束。   
一个`transition`一次包含当前状态、输入、输出和下一个状态向量。一个`transition`是与给定的AIG逻辑一致的，如果模拟的结果是当前状态向量在三值逻辑中的输入向量产生给定的输出和下一个状态。在ASCII表示的`transition`中，四个向量的字符串用空格字符隔开，两个字符串之间正好是一个空格。这意味着“L=0”组合电路的`transition`的开始和结束都是一个空格；没有输入的组合电路以两个空格开始。
一条`trace`由一个`transition`列表构成。若一条`trace`中的所有`transition`是连续的，且所有`transition`(除第一个外)的当前状态向量是和之前的`transition`的下一状态向量相同，则称该`trace`是连续的。若一条`trace`中的第一个`transiton`的当前状态向量只包含`0`，则称这条`trace`已被初始化。`trace`文件中一个`transition`占据一行，使用换行符分隔和标识文件结束。    
因此，`simulator`将AIG和匹配AIG类型的`stimulus`作为输入，并生成一个初始化的连续`trace`。一个随机`simulator`将使用随机输入向量，不需要`stimulus`。   
`x`值不应解释为`don't care`。例如，如果将文字`l`赋值为值`x`，则`l & !l`在三值模拟中会产生`x`，而不是`0`。这个三值逻辑标准的语义允许在对输入进行全局三值分配的情况下对电路进行线性时间模拟。模拟二值逻辑中的部分赋值，也就是检查输出是否固定到某个值，是一个NP完全问题。另一方面，三值模拟是纯粹的句法，优化AIG不需要保留三值模拟语义。   
由于三值模拟的句法性质，我们可以定义`grounded stimulus`的概念，也就是不包含`x`值的`stimulus`。一个`stimulus`是另一个`stimulus`的实例，如果前者与后者(在后者包含`x`的对应位置以外)都相同。前者可以是(`0`、`1`或`x`)这三个值中的任何一个。   
一个`witness`指的是系统可以产生一个坏态`bad state`。   
一个SAT求解问题的`solution`是一个文件，该文件包含一行验证结果(`a result line`)和一个可选的`stimulus`部分。验证结果若是一个`0`则指示该AIG文件无法输出`1`；无效的验证结果行或空文件被解释为未知(无法验证)；结果若是为1，则产生一个坏态的`witness`。

## 11.相关工作
- AIG文件描述
  - [Robust boolean reasoning for equivalence checking and functional property verification](https://www.research.ibm.com/haifa/projects/verification/SixthSense/papers/brn_itcad_02.pdf)
  - [Circuit-based Boolean Reasoning](https://www.research.ibm.com/haifa/projects/verification/SixthSense/papers/brn_dac_01.pdf)
- SAT solver
  - [Symbolic reachability analysis based on SAT-solvers](https://link.springer.com/content/pdf/10.1007/3-540-46419-0_28.pdf)
