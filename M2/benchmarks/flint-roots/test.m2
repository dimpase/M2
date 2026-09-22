load "flintRoots.m2";
checkRoots := (p, bits, n) -> (
    z := flintRoots(p, Precision => bits);
    assert(#z == n);
    assert all(z, a -> precision a == bits);
    assert all(z, a -> abs(sub(p,{(ring p)_0 => a})) < 2.^(-min(bits-10,100)));
    z);
R = ZZ[x]; checkRoots(x^5-1,53,5);
R = QQ[x]; checkRoots(x^2-1/3,150,2);
assert(#flintRoots((x^2-1)/x) == 2);
R = RR_100[x]; checkRoots(x^2-0.1p100,100,2);
R = CC_100[x]; checkRoots(x^2-ii,100,2);
checkRoots((x-(1+2*ii))^4,100,4);
R = QQ[x]; checkRoots(x*(x-1)^3,150,4);
assert(#flintRoots(7_R) == 0);
assert(try flintRoots(0_R) then false else true);
R = QQ[x,y]; assert(#flintRoots(y^2-1) == 2);
assert(try flintRoots(x+y) then false else true);
print "PASS: ZZ, QQ, RR, CC, precision, multiplicities, zero roots, constants, rational functions, and multivariable frontend";
exit 0
