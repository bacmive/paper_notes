#### 互斥协议——不变式、规则和因果关系   
 公式、规则和因果关系对应表    
$$
  \begin{array}{l}
      \text{序号}\ &\text{公式}\ & \text{规则}\ & \text{因果关系}\ & \text{新不变式}\\
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

依据上表，可得出5个不变式的依赖图<br>
不变式：   
$$
    \begin{array}{l}
        1. mutualInv(i,j)\\
        2. invOnXC(i)\\
        3.aux_1(i,j)\\
        4.invOnXE(i)\\
        5.aux_2(i,j)
    \end{array}
$$
依赖图为   
![Alt text](./relation.png)   
> 图中包含由不变式1指向不变式2的箭头，因为上表有:
>$$
    \begin{array}{c}
        \ &mutualInv(1,2)\ & Crit[1]\ & invHoldForRule_3\ &invOnXC(2)\\
        \ &mutualInv(1,2)\ & Crit[2]\ & invHoldForRule_3\ &invOnXC(1)\\
    \end{array}
>$$
>即$invOnXC9i)可以由$$mutualInv(i,j)$经规则$Crit(i)$迁移得到