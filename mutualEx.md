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
3. &invHoldRule_3(s, f, r, fs)\ \equiv\ & \exists f'\in fs\ s.t.\ s\models (f'\land (pre(r))) &\longrightarrow s\models preCond(f, act(r))\\
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

##### 一.   
算法初始化：新建集合$A \leftarrow F$(表示已找到的不变式)，新建数组$tuples=[\  ]$(表示规则和不变式的因果关系)，新建队列$newInvs\leftarrow F$(表示新找到的不变式)，即有:<br>
$A=\{mutualInv(i_1, i_2) \};\  newInvs=\{mutualInv(i_1, i_2)\}$


##### 二.
将队列$newInvs$中的一个元素出队，并将该元素记为$f$，即:$f\leftarrow newInvs.dequeue$，则有:
$$ f \equiv\ mutualInv(i_1, i_2) $$

##### 三.
对于上述公式$f$，分别考虑规则集合$R$中的所有规则。
$$R=\{ Try(j), Crit(j), Exit(j), Idle(j)\} $$

##### 四.
选出$R$中的一条规则$r$，将公式$f$和规则$r$具体化(Concretize)。具体而言：<br>
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

##### 五.
对于每一种具体化方式(以上共12种)，考虑该具体化方式下是否能够产生新的不变式(使用semi-algorithm)，具体而言：<br>
1. 对于公式$f=mutualInv(1,2), 规则r=Try(1)$，<br> 公式$f$相对于规则$r$的最弱前置条件为$preCond(mutualInv(1,2), action(Try(1)))$<br>因为
 $$\begin{array}{l} 
        s\models guard(Try(1)) \vdash s\models preCond(mutualInv(1,2), action(Try(1)))\\
        \Longleftrightarrow  s\models a[1] = I\  \vdash\  s\models \neg((T=C)\land (a[2]=C))
    \end{array}
 $$
始终成立(永真式)(通过定理证明器来实现)<br>
故$(mutualInv(1,2),Try(1))$存在因果关系$invHoldRule_1$，且没有新的不变式产生，只将元组$(mutualInv(1,2),Try(1),invHoldRule_1)$加入$tuples$数组。
    
2. 对于公式$f=mutualInv(1,2), 规则r=Try(2)$，<br> 
同上，没有新的不变式产生，将元组$(mutualInv(1,2),Try(2),invHoldRule_1)$加入$tuples$数组。
    
3. 对于公式$f=mutualInv(1,2), 规则r=Try(3)$，<br> 公式$f$相对于规则$r$的最弱前置条件为$preCond(mutualInv(1,2), action(Try(3)))$<br>
且规则$r=Try(3)$等价于$r=Try(j),\ j\neq 1\ \land j\neq 2$;<br>
所以有
$$\begin{array}{l}
    mutualInv(1,2) = preCond(mutualInv(1,2), action(Try(3)))\\
    \Longrightarrow s\models mutualInv(1,2) \longleftrightarrow  s\models preCond(mutualInv(1,2), action(Try(3)))
    \end{array}
$$
始终成立，故$(mutualInv(1,2),Try(3))$存在因果关系$invHoldRule_2$,且没有新的不变式产生，将元组$(mutualInv(1,2),Try(3),invHoldRule_2)$加入$tuples$数组。
    
4. 对于公式$f=mutualInv(1,2)$, 规则$r=Crit(1)$<br>
公式$f$关于规则$r$的最弱前置条件$preCond(mutualInv(1,2), action(Crit(1))) = \neg(C=C\land a[2]=C)$，<br>
因为
$$
\begin{array}{l}
guard(Crit(1)) \longrightarrow preCond(mutualInv(1,2), action(Crit(1)))\\
\Longleftrightarrow a[1] =T\land x=true \longrightarrow \neg(C=C\land a[2]=C)\\
\text{不是永真式，故不存在}invHoldRule_1\text{关系}\\
\\
mutualInv(1,2) \longrightarrow preCond(mutualInv(1,2), action(Crit(1)))\\
\Longleftrightarrow \neg(a[1]=C\land a[2]=C) \longrightarrow \neg(C=C\land a[2]=C)\\
\text{不是永真式，故不存在}invHoldRule_2\text{关系}
\end{array}
$$
故假设公式$f$和规则$r$存在因果关系$invHoldRule_3$，根据invFind算法可以尝试**构造新的不变式**，构造过程如下：<br>
a. 首先构造析取式：$\neg guard(Crit(1))\lor preCond(mutualInv(1,2), action(Crit(1)))$，<br>即$\neg (a[1]=T\land x=true)\lor \neg (C=C \land a[2]=C)$<br>
b. 上述析取式等价于：$\neg (a[1] = T \land x=true \land C=C\land a[2] =C)$，<br>令$f_1 \equiv a[1] = T,\ f_2\equiv x=true\ f_3\equiv C=C\ f_4\equiv a[2] =C$，即上述公式等价为$\neg(f_1\land f_2\land f_3\land f_4)$<br>
c. 考虑上述公式的子公式$\neg f_1$,$\neg f_2$, $\neg (f_1\land f_2)$,$\neg(f_1\land f_3)$,$\dots$,$\neg(f_1 \land f_2 \land f_3)\dots$。对于每个子公式，使用模型检测工具Murphi或NuSMV检测该子公式是否为该协议实例的不变式，然后进行简化。<br>
d. 经过上一步骤，可以得到一个不变式$invOnXC(2) \equiv \neg(x=true\land a[2]=C)$，通过$isNew$程序检查该不变式是否为新的不变式(permutation symmetry)。<br>
e. 生成的不变式是新的不变式，则将新得到的不变式$invOnXC(2)$进行***一般化(Generalize)***, 得到一般化后的不变式$invOnXC(i_2)$<br>
f. 将元组$(mutualInv(1,2), Crit(1), invHoldRule_3, invOnXC(2))$加入到 $tuples$ 数组中<br>
g. 通过$get$函数处理$invOnXC(i_2)$，得到不变式$invOnXC(i)$。将$invOnXC(i)$加入$newInvs$队列，并加入到集合$A$中。<br>
    
5. 对于公式$f=mutualInv(1,2)$, 规则$r=Crit(2)$<br>
同上，同理可得到一个不变式$invOnXC(1) \equiv \neg(x=true\land a[1]=C)$，通过$isNew$程序检查该不变式不是新的不变式<br>
由于不是新不变式，则只将元组$(mutualInv(1,2), Crit(1), invHoldRule_3, invOnXC(1))加入到 $tuples$ 数组中；

6. 对于公式$f=mutualInv(1,2)$, 规则$r=Crit(3)$<br>公式$f$相对于规则$r$的最弱前置条件为$preCond(mutualInv(1,2), action(Crit(3)))$<br>
由于
$$
    \begin{array}{l}
        mutualInv(1,2) = preCond(mutualInv(1,2), action(Crit(3)))
    \end{array}
$$
所以公式$f=mutualInv(1,2)$, 规则$r=Crit(3)$满足关系$invHoldRule_2$，没有新的不变式产生，将元组$(mutualInv(1,2),Crit(3),invHoldRule_2)$加入$tuples$数组
    
7. 对于公式$f=mutualInv(1,2)$，规则$r=Exit(1)$<br>公式$f$相对于规则$r$的最弱前置条件为$preCond(mutualInv(1,2), action(Exit(1)))$<br>
因为
$$
    \begin{array}{l}
        s\models guard(Exit(1)) \vdash s\models preCond(mutualInv(1,2), action(Exit(1)))\\
        \Longleftrightarrow s\models a[1] = C \vdash s\models \neg(E=C\land a[2]=C)
    \end{array}
$$
始终成立<br>
故$(mutualInv(1,2),Exit(1))$存在因果关系$invHoldRule_1$，且没有新的不变式产生，只将元组$(mutualInv(1,2),Exit(1),invHoldRule_1)$加入$tuples$数组。

8. 对于公式$f=mutualInv(1,2)$，规则$r=Exit(2)$<br>
同上，同理可得$(mutualInv(1,2),Exit(2))$存在因果关系$invHoldRule_1$，没有新的不变式产生，只将元组$(mutualInv(1,2),Exit(2),invHoldRule_1)$加入$tuples$数组。
    
9. 对于公式$f=mutualInv(1,2)$，规则$r=Exit(3)$<br>公式$f$相对于规则$r$的最弱前置条件为$preCond(mutualInv(1,2), action(Exit(3)))$<br>
且规则$r=Exit(3)$等价于$r=Exit(j),\ j\neq 1\ \land j\neq 2$;<br>
所以有
$$\begin{array}{l}
   mutualInv(1,2) = preCond(mutualInv(1,2), action(Exit(3)))\\
   \Longrightarrow s\models mutualInv(1,2) \longleftrightarrow  s\models preCond(mutualInv(1,2), action(Exit(3)))
   \end{array}
$$
始终成立，故$(mutualInv(1,2),Exit(3))$存在因果关系$invHoldRule_2$,且没有新的不变式产生，将元组$(mutualInv(1,2),Exit(3),invHoldRule_2)$加入$tuples$数组。
    
10. 对于公式$f=mutualInv(1,2)$，规则$r=Idle(1)$<br>公式$f$相对于规则$r$的最弱前置条件为$preCond(mutualInv(1,2), action(Idle(1)))$<br>
因为
$$
   \begin{array}{l}
       s\models guard(Idle(1)) \vdash s\models preCond(mutualInv(1,2), action(Idle(1)))\\
       \Longleftrightarrow s\models a[1] = E \vdash s\models \neg(I=C\land a[2]=C)
   \end{array}
$$
始终成立<br>
故$(mutualInv(1,2),Idle(1))$存在因果关系$invHoldRule_1$，且没有新的不变式产生，只将元组$(mutualInv(1,2),Idle(1),invHoldRule_1)$加入$tuples$数组。

11. 对于公式$f=mutualInv(1,2)$，规则$r=Idle(2)$<br>
同上，同理可得$(mutualInv(1,2),Idle(2))$存在因果关系$invHoldRule_1$，没有新的不变式产生，只将元组$(mutualInv(1,2),Idle(2),invHoldRule_1)$加入$tuples$数组。

12. 对于公式$f=mutualInv(1,2)$，规则$r=Idle(3)$<br>公式$f$相对于规则$r$的最弱前置条件为$preCond(mutualInv(1,2), action(Idle(3)))$<br>
且规则$r=Idle(3)$等价于$r=Idle(j),\ j\neq 1\ \land j\neq 2$;<br>
所以有
$$\begin{array}{l}
    mutualInv(1,2) = preCond(mutualInv(1,2), action(Idle(3)))\\
    \Longrightarrow s\models mutualInv(1,2) \longleftrightarrow  s\models preCond(mutualInv(1,2), action(Idle(3)))
    \end{array}
$$
始终成立，故$(mutualInv(1,2),Idle(3))$存在因果关系$invHoldRule_2$,且没有新的不变式产生，将元组$(mutualInv(1,2),Idle(3),invHoldRule_2)$加入$tuples$数组。
    
##### 六.     
考虑完不变式$mutualInv(1,2)$和规则集$R$中的每个规则之后，从不变式队列$newInvs$中继续取出新产生的不变式(本程序循环至$newInvs$队列为空为止)。即$f=newInvs.dequeue$，得$f=invOnXC(i)$<br>
##### 七.    
依次选出公式集$R$中的每一条规则$r$，将公式$f$和规则$r$具体化。具体如下：<br>
对于公式$f=invOnXC(i)$和规则$r=Try(j)$，这两者的具体化方式有如下两种：
$$ \begin{array}{l}
        \text{令} i=1,\ f = invOnXC(1);\ & \text{令} j=1,\ r=Try(1);\\
        \text{令} i=1,\ f = invOnXC(1);\ & \text{令} j=2,\ r=Try(2);
    \end{array}
$$   
对于公式$f=invOnXC(i)$和规则$r=Crit(j)$，这两者的具体化方式有如下两种：
$$ \begin{array}{l}
        \text{令} i=1,\ f = invOnXC(1);\ & \text{令} j=1,\ r=Crit(1);\\
        \text{令} i=1,\ f = invOnXC(1);\ & \text{令} j=2,\ r=Crit(2);
    \end{array}
$$  
对于公式$f=invOnXC(i)$和规则$r=Exit(j)$，这两者的具体化方式有如下两种：
$$ \begin{array}{l}
        \text{令} i=1,\ f = invOnXC(1);\ & \text{令} j=1,\ r=Exit(1);\\
        \text{令} i=1,\ f = invOnXC(1);\ & \text{令} j=2,\ r=Exit(2);
    \end{array}
$$  
对于公式$f=invOnXC(i)$和规则$r=Idle(j)$，这两者的具体化方式有如下两种：
$$ \begin{array}{l}
        \text{令} i=1,\ f = invOnXC(1);\ & \text{令} j=1,\ r=Idle(1);\\
        \text{令} i=1,\ f = invOnXC(1);\ & \text{令} j=2,\ r=Idle(2);
    \end{array}
$$  
##### 八.   
对于每一种具体化方式(以上共8种)，考虑该具体化方式下是否能够产生新的不变式，具体如下：
1. 对于公式$f=invOnXC(1)$, 规则$r=Try(1)$，<br> 
公式$f$相对于规则$r$的最弱前置条件为$preCond(invOnXC(1), action(Try(1)))$<br>
因为
$$
\begin{array}{l}
    s\models guard(Try(1)) \longrightarrow s\models preCond(invOnXC(1), action(Try(1)))\\
    \Longleftrightarrow s\models a[1] = I \longrightarrow \neg(x=true\land T=C)
\end{array}
$$
始终成立，
故$(invOnXC(1), Try(1))$之间存在因果关系$invHoldRule_1$，且没有新的不变式产生，将因果关系元组$(invOnXC(1), Try(1),invHoldRule_1)$加入到$tuples$数组中。
    
2. 对于公式$f=invOnXC(1)$, 规则$r=Try(2)$，<br> 
公式$f$相对于规则$r$的最弱前置条件为$preCond(invOnXC(1), action(Try(2)))$<br>
且规则$Try(2)$等价于$Try(j),\ j\neq 1$<br>
所以有
$$
\begin{array}{l}
    invOnXC(1) \equiv preCond(invOnXC(1), action(Try(2)))\\
    \Longrightarrow s\models invOnXC(1) \longleftrightarrow s\models preCond(invOnXC(1), action(Try(2)))
\end{array}
$$
始终成立，故$(invOnXC(1), Try(2))$之间存在因果关系$invHoldRule_2$，且没有新的不变式产生，将因果关系元组$(invOnXC(1), Try(2),invHoldRule_2)$加入到$tuples$数组中。

3. 对于公式$f=invOnXC(1)$, 规则$r=Crit(1)$，<br>
公式$f$相对于规则$r$的最弱前置条件为$preCond(invOnXC(1), action(Crit(1)))$<br>
因为
$$
   \begin{array}{l}
       s\models guard(Crit(1)) \longrightarrow s\models preCond(invOnXC(1), action(Crit(1)))\\
       \Longleftrightarrow s\models a[1] = T\land x=true \longrightarrow \neg(false=true\land C=C)
   \end{array}
$$
始终成立，故$(invOnXC(1), Crit(1))$之间存在因果关系$invHoldRule_1$，且没有新的不变式产生，将因果关系元组$(invOnXC(1), Crit(1),invHoldRule_1)$加入到$tuples$数组中。

4. 对于公式$f=invOnXC(1)$, 规则$r=Crit(2)$，<br>
公式$f$相对于规则$r$的最弱前置条件为$preCond(invOnXC(1), action(Crit(2)))$<br>
且规则$Crit(2)$等价于$Crit(j),\ j\neq 1$<br>
所以有
$$
\begin{array}{l}
    invOnXC(1) \equiv preCond(invOnXC(1), action(Crit(2)))\\
    \Longrightarrow s\models invOnXC(1) \longleftrightarrow s\models preCond(invOnXC(1), action(Crit(2)))
\end{array}
$$
始终成立，故$(invOnXC(1), Crit(2))$之间存在因果关系$invHoldRule_2$，且没有新的不变式产生，将因果关系元组$(invOnXC(1), Crit(2),invHoldRule_2)$加入到$tuples$数组中。
    
5. 对于公式$f=invOnXC(1)$, 规则$r=Idle(1)$，<br>
公式$f$相对于规则$r$的最弱前置条件为$preCond(invOnXC(1), action(Idle(1)))$<br>
$$
\begin{array}{l}
    s\models guard(Idle(1)) \longrightarrow s\models preCond(invOnXC(1), action(Idle(1)))\\
    \Longleftrightarrow s\models a[1] = E \longrightarrow \neg(true=true\land I=C)
\end{array}
$$
始终成立，故$(invOnXC(1), Idle(1))$之间存在因果关系$invHoldRule_1$，且没有新的不变式产生，将因果关系元组$(invOnXC(1), Idle(1),invHoldRule_1)$加入到$tuples$数组中。
    
6. 对于公式$f=invOnXC(1)$, 规则$r=Idle(2)$，<br>
公式$f$关于规则$r$的最弱前置条件$preCond(invOnXC(1), action(Idle(2))) <br>
因为
$$
\begin{array}{l}
    guard(Idle(2)) \longrightarrow preCond(invOnXC(1), action(Idle(2)))\\
    \Longleftrightarrow a[2] =E \longrightarrow \neg(true=true\land a[1]=C)\\
    \text{不是永真式，故不存在}invHoldRule_1\text{关系}\\
    \\
    invOnXC(1) \longrightarrow preCond(invOnXC(1), action(Idle(2)))\\
    \Longleftrightarrow \neg(x=true\land a[1]=C) \longrightarrow \neg(true=true\land a[1]=C)\\
    \text{不是永真式，故不存在}invHoldRule_2\text{关系}
\end{array}
$$
故假设公式$f$和规则$r$存在因果关系$invHoldRule_3$，根据invFind算法可以尝试**构造新的不变式**，构造过程如下：<br>
a. 首先构造析取式：$\neg guard(Idle(2))\lor preCond(invOnXC(1), action(Idle(2)))$，<br>即$\neg (a[2]=E)\lor \neg (true=true\land a[1]=C)$<br>
b. 上述析取式等价于$\neg(a[2]=E \land true=true \land a[1]=C)$，<br>令$f_1 \equiv a[2]=E;\ f_2 \equiv true=true,\ f_3 \equiv a[1]=C$，即上述公式等价为$\neg(f_1\land f_2\land f_3)$<br>
c. 考虑上述公式的子公式$\neg f_1$,$\neg f_2$, $\neg (f_1\land f_2)$,$\neg(f_1\land f_3)$,$\dots$,$\neg(f_1 \land f_2 \land f_3)$。对于每个子公式，使用模型检测工具Murphi或NuSMV检测该子公式是否为该协议实例的不变式，然后进行简化。<br>
d. 经过上一步骤，可以得到一个不变式$aux_1(1,2) \equiv \neg(a[1] =C \land a[2]= E)$，通过$isNew$程序检查该不变式是否为新的不变式(permutation symmetry)。<br>
e. 生成的不变式是新的不变式，则将新得到的不变式$aux_1(1,2)$进行***一般化(Generalize)***, 得到一般化后的不变式$aux_1(i_1,i_2)$，<br>
f. 将元组$(invOnXC(1), Idle(2), invHoldRule_3, aux_1(1, 2))加入到 $tuples$ 数组中<br>
g. 通过$get$函数处理$aux_1(i_1, i_2)$，得到不变式$aux_1(i,j)$。将$aux_1(i,j)$加入$newInvs$队列，并加入到集合$A$中。<br>
   
##### 九. 
继续从$newInvs$队列中取出新的不变式，重复上述过程(第6、7步骤)，直至$newInvs$队列为空。<br>
最终获得的不变式为
$$
\begin{array}{l}
    invOnXC(i) & \equiv  & \neg(x=true\land a[i]=C)&\\
    aux_1(i,j) & \equiv & \neg(a[i]=C\land a[j]=E)&\\
    invOnXE(i) & \equiv & \neg(x=true\land a[i]=E)&\\
    mutualEx(i,j) & \equiv & \neg(a[i]=C\land a[j]=C),&\ \text{system requirement}\\
    aux_2(i,j) & \equiv & \neg(a[i] = E \land a[j] =E)&
\end{array}
$$
    
##### 十.
最终的$tuples$数组中的内容为：
$$
    \begin{array}{l}
        \text{序号}\ &\text{不变式}\ & \text{规则}\ & \text{因果关系}\ & \text{新不变式}\\
        1.\ &mutualInv(1,2)\ & Try[1]\ & invHoldForRule_1\ &\\
        2.\ &mutualInv(1,2)\ & Try[2]\ & invHoldForRule_1\ &\\
        3.\ &mutualInv(1,2)\ & Try[3]\ & invHoldForRule_2\ &\\
        4.\ &mutualInv(1,2)\ & Crit[1]\ & invHoldForRule_3\ &invOnXC(2)\\
        5.\ &mutualInv(1,2)\ & Crit[2]\ & invHoldForRule_3\ &invOnXC(1)\\
        6.\ &mutualInv(1,2)\ & Crit[3]\ & invHoldForRule_2\ &\\
        7.\ &mutualInv(1,2)\ & Exit[1]\ & invHoldForRule_1\ &\\
        8.\ &mutualInv(1,2)\ & Exit[2]\ & invHoldForRule_1\ &\\
        9.\ &mutualInv(1,2)\ & Exit[3]\ & invHoldForRule_2\ &\\
        10.\ &mutualInv(1,2)\ & Idle[1]\ & invHoldForRule_1\ &\\
        11.\ &mutualInv(1,2)\ & Idle[2]\ & invHoldForRule_1\ &\\
        12.\ &mutualInv(1,2)\ & Idle[3]\ & invHoldForRule_2\ &\\
        13.\ &invOnXC(1)\ & Try[1]\ & invHoldForRule_1\ &\\
        14.\ &invOnXC(1)\ & Try[2]\ & invHoldForRule_2\ &\\
        15.\ &invOnXC(1)\ & Crit[1]\ & invHoldForRule_1\ &\\
        16.\ &invOnXC(1)\ & Crit[2]\ & invHoldForRule_1\ &\\
        17.\ &invOnXC(1)\ & Exit[1]\ & invHoldForRule_1\ &\\
        18.\ &invOnXC(1)\ & Exit[2]\ & invHoldForRule_2\ &\\
        19.\ &invOnXC(1)\ & Idle[1]\ & invHoldForRule_1\ &\\
        20.\ &invOnXC(1)\ & Idle[2]\ & invHoldForRule_3\ &aux_1(1,2)\\
        21.\ &aux_1(2,1)\ & Try[1]\ & invHoldForRule_1\ &\\
        22.\ &aux_1(2,1)\ & Try[2]\ & invHoldForRule_1\ &\\
        23.\ &aux_1(2,1)\ & Try[3]\ & invHoldForRule_2\ &\\
        24.\ &aux_1(2,1)\ & Crit[1]\ & invHoldForRule_1\ &\\
        25.\ &aux_1(2,1)\ & Crit[2]\ & invHoldForRule_3\ &invOnXE(1)\\
        26.\ &aux_1(2,1)\ & Crit[3]\ & invHoldForRule_2\ &\\
        27.\ &aux_1(2,1)\ & Exit[1]\ & invHoldForRule_3\ &mutualInv(1,2)\\
        28.\ &aux_1(2,1)\ & Exit[2]\ & invHoldForRule_1\ &\\
        29.\ &aux_1(2,1)\ & Exit[3]\ & invHoldForRule_2\ &\\
        30.\ &aux_1(2,1)\ & Idle[1]\ & invHoldForRule_1\ &\\
        31.\ &aux_1(2,1)\ & Idle[2]\ & invHoldForRule_1\ &\\
        32.\ &aux_1(2,1)\ & Idle[3]\ & invHoldForRule_2\ &\\
        33.\ &invOnXE(1)\ & Try[1]\ & invHoldForRule_1\ &\\
        34.\ &invOnXE(1)\ & Try[2]\ & invHoldForRule_2\ &\\
        35.\ &invOnXE(1)\ & Crit[1]\ & invHoldForRule_1\ &\\
        36.\ &invOnXE(1)\ & Crit[2]\ & invHoldForRule_1\ &\\
        37.\ &invOnXE(1)\ & Exit[1]\ & invHoldForRule_3\ &invOnXC(1)\\
        38.\ &invOnXE(1)\ & Exit[2]\ & invHoldForRule_2\ &\\
        39.\ &invOnXE(1)\ & Idle[1]\ & invHoldForRule_1\ &\\
        40.\ &invOnXE(1)\ & Idle[2]\ & invHoldForRule_3\ &aux_2(1,2)\\
        41.\ &aux_2(2,1)\ & Try[1]\ & invHoldForRule_1\ &\\
        42.\ &aux_2(2,1)\ & Try[2]\ & invHoldForRule_1\ &\\
        43.\ &aux_2(2,1)\ & Try[3]\ & invHoldForRule_2\ &\\
        44.\ &aux_2(2,1)\ & Crit[1]\ & invHoldForRule_1\ &\\
        45.\ &aux_2(2,1)\ & Crit[2]\ & invHoldForRule_1\ &\\
        46.\ &aux_2(2,1)\ & Crit[3]\ & invHoldForRule_2\ &\\
        47.\ &aux_2(2,1)\ & Exit[1]\ & invHoldForRule_3\ &aux_1(1,2)\\
        48.\ &aux_2(2,1)\ & Exit[2]\ & invHoldForRule_3\ &aux_1(2,1)\\
        49.\ &aux_2(2,1)\ & Exit[3]\ & invHoldForRule_2\ &\\
        50.\ &aux_2(2,1)\ & Idle[1]\ & invHoldForRule_1\ &\\
        51.\ &aux_2(2,1)\ & Idle[2]\ & invHoldForRule_1\ &\\
        52.\ &aux_2(2,1)\ & Idle[3]\ & invHoldForRule_2\ &\\
    \end{array}
$$
        
        
