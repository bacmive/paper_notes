(可以用马克飞象或cmdmarkdown在线转换成pdf)
## 互斥协议——归纳不变式的生成

互斥协议`P`： 含`N`个节点 ，节点之间按一定规则互斥地访问临界资源。 其中的每个节点都包含4种状态`{Idle,Trying,Critical,Exiting} `，使用数组变量`a[N]`表示每个节点所处状态，`a[i]=I`表示节点`i`处于`Idle`状态。本文取`N=2`。全局变量`x`标识临界资源是否空闲。    



###  1. 协议组成   

##### 1.1 协议的规则(卫式，guard command)  

$$
\begin{array}{c}
Try(i) \equiv\ & a[j] = I\ & \vartriangleright\ & a[j]:=T \\
Crit(j) \equiv\ & x=true\land a[j]=T\ & \vartriangleright\ &\{ a[j]:=C,x:=false\}\\
Exit(j) \equiv\ & a[j]=C\ & \vartriangleright\ & a[j]:=E\\
Idle(j) \equiv\ & a[j]=E\ & \vartriangleright\ & \{ a[j]:=I, x:=true \}
\end{array}\\ 
$$
$$
\text{每一规则形如}r \equiv g\vartriangleright a, \text{则记}guard(r) = g ,\ action(r) = a
$$

##### 1.2 协议的初始状态(N=2)  

$$
mutexini_N\ \equiv\ x=true\land\bigwedge_{i=1}^Na[i]=I
$$

##### 1.3 协议的规则集(N=2)

$$
mutexrules_N\ = \{ try(j), crit(j), exit(j), idle(j)\ |\ j=1,\dots,N\}
$$

##### 1.4 协议的定义(N=2)

$$
mutualEx_N\ =\ (mutexini_N, mutexrules_N)
$$

#####  1.5 协议的设计要求(不变式)

$$
mutualInv(i_1, i_2)\ \equiv\ \neg(a[i_1]=C\land a[i_2]=C),\ i_1\neq i_2
$$





### 2. 因果关系(casual relations)

$$
\begin{array}{c}
1.& invHoldRule_1(s,f,r)\ \equiv\ & s \models pre(r) &\longrightarrow s\models preCond(f,act(r)) \\
2. &invHoldRule_2(s,f,r)\ \equiv\ & s \models f &\longleftrightarrow s\models preCond(f, act(r))\\
3. &invHoldRule_3(s, f, r, fs)\ \equiv\ & \exist f'\in fs\ s.t.\ s\models (f'\land (pre(r))) &\longrightarrow s\models preCond(f, act(r))\\
\end{array}
$$
合并上述公式，可以得到`(f,r,fs)`三者之间的因果关系的定义如下，其中`f`是一个谓词公式(不变式)，`r`是一个规则(卫式)，`fs`是一个公式集合，`s`表示状态
$$
invHoldRule(s, f, r, fs)\ \equiv\ s\models invHoldRule_1(s,f,r) \lor s\models invHoldRule_2(s,f,r) \lor s\models invHoldRule_3(s,f,r,fs).
$$



### 3. 使用invFinder算法寻找归纳不变式   
$$
\begin{array}{l}
\text{算法输入：} \text{初始不变式集合F,协议模型P=(I,R);}\\
                 \quad \quad \quad \quad \quad \text{本例中}F=\{mutualInv(i_2,i_2)\}, I=mutexini_N(N=2), R=mutexrules_N(N=2)\\
\text{算法输出：} \text{具体规则和不变式之间的因果关系}
\end{array}
$$

#### 3.1 算法实现步骤   

0.  算法初始化：新建集合$A \leftarrow F$(表示已找到的不变式)，新建数组$tuples=[\  ]$(表示已找到的规则和不变式的因果关系)，新建队列$newInvs\leftarrow F$(表示新找到的不变式)，即有:<br>
           $A=\{mutualInv(i_1, i_2) \};\  newInvs=\{mutualInv(i_1, i_2)\}$

1. 取出$newInvs$中的一个元素(相当于将队列$newInvs$中的一个元素出队)，并记为$f$，即:$f\leftarrow newInvs.dequeue$，则$f$有：   
    $$ f \equiv\ mutualInv(i_1, i_2) $$

2. 对于上述公式$f$，分别对规则集合$R$中的所有规则进行考虑。其中:
   $$R=\{ Try(j), Crit(j), Exit(j), Idle(j)\} $$

3. 选出$R$中的一条规则$r$，将公式$f$和规则$r$具体化(Concretize)。具体而言：<br>
   对于公式$f=mutualInv(i_1, i_2)$和规则$r=Try(j)$，这两者的具体化方式有如下三种：
    $$ \begin{array}{l}
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=1,\ r=Try(1);\\
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=2,\ r=Try(2);\\
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=3,\ r=Try(3);
        \end{array}
    $$   
    对于公式$f=mutualInv(i_1, i_2)$和规则$r=Crit(j)$， 具体化方式有如下三种：
    $$ \begin{array}{l}
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=1,\ r=Crit(1);\\
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=2,\ r=Crit(2);\\
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=3,\ r=Crit(3);
        \end{array}
    $$
    对于公式$f=mutualInv(i_1, i_2)$和规则$r=Exit(j)$， 具体化方式有如下三种：
    $$ \begin{array}{l}
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=1,\ r=Exit(1);\\
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=2,\ r=Exit(2);\\
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=3,\ r=Exit(3);
        \end{array}
    $$
    对于公式$f=mutualInv(i_1, i_2)$和规则$r=Idle(j)$， 具体化方式有如下三种：
    $$ \begin{array}{l}
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=1,\ r=Idle(1);\\
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=2,\ r=Idle(2);\\
            \text{令} i_1=1,\ i_2=2,\ f = mutualInv(1,2);\ & \text{令} j=3,\ r=Idle(3);
        \end{array}
    $$

4. 对于每一种具体化方式(以上共12种)，考虑该具体化方式下是否能够产生新的不变式(使用semi-algorithm)，具体而言：<br>
   1. 对于公式$f=mutualInv(1,2), 规则r=Try(1)$，<br> 因为
      $$\begin{array}{l} 
        s\models guard(Try(1)) \vdash s\models preCond(mutualInv(1,2), action(Try(1)))\\
        \Longleftrightarrow  s\models a[1] = I\  \vdash\  s\models \neg((T=C)\land (a[2]=C))
        \end{array}
      $$
      成立(这可以通过定理证明器来实现)<br>
      故$(mutualInv(1,2),Try(1))$存在因果关系$invHoldRule_1$，无新的不变式产生，将元组$(mutualInv(1,2),Try(1),invHoldRule_1)$加入$tuples$数组。
    
    2. 对于公式$f=mutualInv(1,2), 规则r=Try(2)$，<br> 
        同上，无新的不变式产生，将元组$(mutualInv(1,2),Try(2),invHoldRule_1)$加入$tuples$数组。
    
    3. 对于公式$f=mutualInv(1,2), 规则r=Try(3)$，<br>
        规则$r=Try(3)$等价于$r=Try(j),\ j\neq 1\ \land j\neq 2$;<br>
        因为
        $$\begin{array}{l}
            mutualInv(1,2) = preCond(mutualInv(1,2), action(Try(3)))\\
            \Longrightarrow s\models mutualInv(1,2) \longleftrightarrow  s\models preCond(mutualInv(1,2), action(Try(3)))
            \end{array}
        $$
        成立，故$(mutualInv(1,2),Try(3))$存在因果关系$invHoldRule_2$,无新的不变式产生，将元组$(mutualInv(1,2),Try(3),invHoldRule_2)$加入$tuples$数组。
    
    4. 对于公式$f=mutualInv(1,2)$, 规则$r=Crit(1)$<br>
        最弱前置条件$preCond(mutualInv(1,2), action(Crit(1))) = \neg(C=C\land a[2]=C)$，<br>
        因为
        $$
            \begin{array}{l}
                guard(Crit(1)) \nrightarrow mutualInv(1,2), \text{不存在}invHoldRule_1\text{关系}\\
                mutualInv(1,2) \neq preCond(mutualInv(1,2), action()), \text{不存在}invHoldRule_2\text{关系}
            \end{array}
        $$
        故根据invFind算法**构造新的不变式**，构造过程如下：<br>
        1. 首先构造析取式：$\neg guard(Crit(1))\lor preCond(mutualInv(1,2), action(Crit(1)))$，<br>即$\neg (a[1]=T\land x=true)\lor \neg (C=C \land a[2]=C)$
        2. 上述析取式等价于：$\neg (a[1] = T \land x=true \land C=C\land a[2] =C)$，<br>令$f_1 \equiv a[1] = T,\ f_2\equiv x=true\ f_3\equiv C=C\ f_4\equiv a[2] =C$，即上述公式等价为$\neg(f_1\land f_2\land f_3\land f_4)$
        3. 考虑上述公式的子公式$\neg f_1$,$\neg f_2$, $\neg (f_1\land f_2)$,$\neg(f_1\land f_3)$,$\dots$,$\neg(f_1 \land f_2 \land f_2)$。对于每个公式，使用模型检测工具Murphi或NuSMV检测该公式是否为该协议实例的不变式。
        4. 经过上一步骤，得到一个不变式$invOnXC(2) \equiv \neg(x=true\land a[2]=C)$，通过$isNew$程序检查该不变式是否为新的不变式(permutation symmetry)。
        5. 将新得到的不变式$invOnXC(2)$进行***一般化(Generalize)***, 得到一般化后的不变式$invOnXC(i_2)$
        6. 将元组$(mutualInv(1,2), Crit(1), invHoldRule_3, invOnXC(2))加入到 $tuples$ 数组中
        7. 通过$get$函数处理$invOnXC(i_2)$，得到新的不变式$invOnXC(i)$。将$invOnXC(i)$加入$newInvs$队列，并加入到集合$A$中，。
    
    5. 对于公式$f=mutualInv(1,2)$, 规则$r=Crit(2)$<br>
       同上，同理可得到一个不变式$invOnXC(1) \equiv \neg(x=true\land a[1]=C)$通过$isNew$程序检查该不变式是否为新的不变式（不是）<br>
       由于不是新不变式，则只将元组$(mutualInv(1,2), Crit(1), invHoldRule_3, invOnXC(1))加入到 $tuples$ 数组中；

    6. 对于公式$f=mutualInv(1,2)$, 规则$r=Crit(3)$<br>
        由于
        $$
            \begin{array}{l}
                mutualInv(1,2) = preCond(mutualInv(1,2), action(Crit(3)))
            \end{array}
        $$
        所以公式$f=mutualInv(1,2)$, 规则$r=Crit(3)$满足关系$invHoldRule_2$，无新的不变式产生，将元组$(mutualInv(1,2),Crit(3),invHoldRule_2)$加入$tuples$数组