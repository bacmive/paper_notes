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
> 包含如下两行的AIG文件代表常量`FALSE` ,其中`header`(第一行)中的1代表输出的个数为1，第二行代表唯一的输出，输出是一个`literal`
```
aag 0 0 0 1 0				header
0							output
```
> 如下AIG文件代表常量`TRUE`
```
aag 0 0 0 1 0				header
1							output
```
> 下述文件是一个`buffer`， 其中第一个数1为最大变量下标(`maximal variable index`)，第二个数1代表输入个数，
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




