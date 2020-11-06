(*
    newInvs : new Invariants(initialized to empty set)
    invs    : invariants(initialized to empty set)
    casRel  : all the causal relations constructed up to now 
*)
let findInvsFromRule chk choose tautchk isNew pRule paras inv newInvs invs casRel = 
    let rule = ruleApp pRule paras in
    let val (g, S) = rule in
    let inv' = preCond S inv in (* computing the pre-condition *)
        if inv = inv'  (* case analysis on inv' *)
            then let relItem = (pRule, paras, inv, invHoldForRule2 inv r) in
                 (newInvs, relItem::casRel)
        else if tautchk(g -> inv') 
            then  let relItem = (pRule, paras, inv, invHoldForRule1, inv, r) in
                  (newInvs, relItem::casRel)
        else  
            (* choose a new auxiliary invariant from the conjuncts of g & !inv' *)
            (* call the function chk to guarantee newInv is an invariant of the reference model*)
            let newInv = choose chk inv' g in 
            let relItem = (pRule, paras, inv, invHoldForRule3 inv newInv) in
            (* isNew is used to check whether the invariant is new *)
            (* the meaning of the word “new” is modulo to the symmetry relation*)
            if (isNew newInv (newInvs@invs)) 
                then (newInvs@[normalize newInv], relItem::casRel)
            else
                error "no new invariant"
