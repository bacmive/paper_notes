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
>锁存器通常被初始化为0。下面使用了“使能信号”`enable`和额外的低电平复位输入，实现了上述振荡电路
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


