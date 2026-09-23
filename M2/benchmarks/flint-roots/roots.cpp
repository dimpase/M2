// Experimental root backend: exact squarefree decomposition, then Acb isolation.
// This standalone harness mirrors the coefficient setters in rawRoots.
#include <cstdio>
#include <cstdlib>
#include <mpfr.h>
#include <flint/acb_poly.h>
#include <flint/fmpq_poly.h>
#include <flint/fmpz_poly_factor.h>
#include <flint/gr_poly.h>
#include <flint/gr_vec.h>
#include <flint/fmpq.h>
#include <flint/nf_elem.h>
#include <flint/nf.h>
#define register
#include <mps/mps.h>
#undef register
#include <gmpxx.h>
#include <chrono>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <string>

static void check_impl(int status, int line) { if (status) throw std::runtime_error("FLINT status " + std::to_string(status) + " at line " + std::to_string(line)); }
#define check(s) check_impl((s), __LINE__)
struct Ball {
    acb_t z;
    Ball() { acb_init(z); }
    Ball(const Ball& b) { acb_init(z); acb_set(z,b.z); }
    Ball& operator=(const Ball& b) { acb_set(z,b.z); return *this; }
    ~Ball() { acb_clear(z); }
};
struct Coeff { mpq_class re, im; };
static double seconds() {
    return std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count();
}
static void roundq(mpq_class& q, long bits) {
    mpfr_t x; mpfr_init2(x,bits); mpfr_set_q(x,q.get_mpq_t(),MPFR_RNDN);
    mpfr_get_q(q.get_mpq_t(),x); mpfr_clear(x);
}
static slong next_precision(slong wp, long bits, bool machine_start) {
    const slong target=std::max(64L,bits+32);
    return machine_start && wp<target ? std::min(2*wp,target) : 2*wp;
}
static std::vector<Ball> flint_roots(const std::vector<Coeff>& a, long bits,
                                    double& preprocessing, long& workprec, bool machine_start) {
    bool real=true; for (const auto& c:a) real &= c.im==0;
    // Isolating all n roots itself certifies squarefreeness. Try this first for
    // complex input, avoiding an expensive exact Q(i) gcd in the common case.
    if (!real) {
        slong n=a.size()-1; acb_ptr r=_acb_vec_init(n);
        acb_poly_t b; acb_poly_init(b); fmpq_t q; fmpq_init(q);
        bool success=false, have_initial=false;
        slong wp=machine_start?53:std::max(64L,bits+32);
        for(;wp<=2*std::max(64L,bits+32);wp=next_precision(wp,bits,machine_start)) {
            workprec=std::max(workprec,wp);
            acb_poly_fit_length(b,n+1); _acb_poly_set_length(b,n+1);
            for(slong j=0;j<=n;++j) {
                fmpq_set_mpq(q,a[j].re.get_mpq_t()); arb_set_fmpq(acb_realref(b->coeffs+j),q,wp);
                fmpq_set_mpq(q,a[j].im.get_mpq_t()); arb_set_fmpq(acb_imagref(b->coeffs+j),q,wp);
            }
            success=acb_poly_find_roots(r,b,have_initial?r:nullptr,std::max(100L,4*n),wp)==n;
            have_initial=true;
            for(slong j=0;j<n;++j) {
                have_initial &= acb_is_finite(r+j);
                success &= acb_is_finite(r+j) && (acb_is_zero(r+j)||acb_rel_accuracy_bits(r+j)>=bits);
            }
            if(success) break;
        }
        std::vector<Ball> result;
        if(success) for(slong j=0;j<n;++j) {result.emplace_back(); acb_set(result.back().z,r+j);}
        _acb_vec_clear(r,n); acb_poly_clear(b); fmpq_clear(q);
        if(success) {preprocessing=0; return result;}
    }
    gr_ctx_t Q,K,P,Z,A;
    fmpq_poly_t modulus, coeff; fmpq_poly_init(modulus); fmpq_poly_init(coeff);
    fmpq_poly_set_coeff_si(modulus,0,1); fmpq_poly_set_coeff_si(modulus,2,1);
    nf_t nf; if (!real) nf_init(nf,modulus);
    gr_ctx_init_fmpq(Q);
    if (real) gr_ctx_init_fmpq(K); else gr_ctx_init_nf(K,modulus);
    gr_ctx_init_gr_poly(P,K); gr_ctx_init_fmpz(Z);
    gr_poly_t p; gr_poly_init(p,K);
    gr_ptr c=gr_heap_init(K), v=gr_heap_init(K), unit=gr_heap_init(K), leading=gr_heap_init(K);
    fmpq_t q; fmpq_init(q);
    if (!real) check(gr_gen(unit,K));
    for (size_t j=0;j<a.size();++j) {
        fmpq_set_mpq(q,a[j].re.get_mpq_t()); check(gr_set_fmpq(c,q,K));
        if (!real) {
            fmpq_set_mpq(q,a[j].im.get_mpq_t()); check(gr_mul_fmpq(v,unit,q,K));
            check(gr_add(c,c,v,K));
        }
        check(gr_poly_set_coeff_scalar(p,j,c,K));
    }
    gr_vec_t factors, exponents; gr_vec_init(factors,0,P); gr_vec_init(exponents,0,Z);
    if (real) {
        // The generic rational Euclidean gcd suffers severe coefficient growth.
        // Clear denominators and use FLINT's specialized integer algorithm.
        fmpq_poly_t rational; fmpq_poly_init(rational);
        for(size_t j=0;j<a.size();++j) {
            fmpq_set_mpq(q,a[j].re.get_mpq_t()); fmpq_poly_set_coeff_fmpq(rational,j,q);
        }
        fmpz_poly_t integer; fmpz_poly_init(integer); fmpq_poly_get_numerator(integer,rational);
        fmpz_poly_factor_t sf; fmpz_poly_factor_init(sf); fmpz_poly_factor_squarefree(sf,integer);
        gr_poly_t factor; gr_poly_init(factor,K); fmpz_t exponent; fmpz_init(exponent);
        for(slong j=0;j<sf->num;++j) {
            check(gr_poly_set_fmpz_poly(factor,sf->p+j,K)); check(gr_vec_append(factors,factor,P));
            fmpz_set_si(exponent,sf->exp[j]); check(gr_vec_append(exponents,exponent,Z));
        }
        fmpz_clear(exponent); gr_poly_clear(factor,K); fmpz_poly_factor_clear(sf);
        fmpz_poly_clear(integer); fmpq_poly_clear(rational);
    } else check(gr_poly_factor_squarefree(leading,factors,exponents,p,K));
    preprocessing=seconds()-preprocessing;
    std::vector<Ball> out;
    for (slong k=0;k<factors->length;++k) {
        auto f=(gr_poly_struct*)gr_vec_entry_ptr(factors,k,P);
        slong n=f->length-1;
        slong mult=fmpz_get_si((fmpz*)gr_vec_entry_ptr(exponents,k,Z));
        acb_ptr r=_acb_vec_init(n);
        acb_poly_t b; acb_poly_init(b);
        bool success=false, have_initial=false;
        // Reconvert exact coefficients at each precision. Never freeze input balls.
        for (slong wp=machine_start?53:std::max(64L,bits+32);wp<=32768;wp=next_precision(wp,bits,machine_start)) {
            workprec=std::max(workprec,wp);
            gr_ctx_init_complex_acb(A,wp);
            acb_poly_fit_length(b,f->length);
            for(slong j=0;j<f->length;++j) {
                check(gr_poly_get_coeff_scalar(c,f,j,K));
                if (real) check(gr_set_other(b->coeffs+j,c,K,A));
                else {
                    nf_elem_get_fmpq_poly(coeff,(nf_elem_struct*)c,nf);
                    fmpq_poly_get_coeff_fmpq(q,coeff,0); arb_set_fmpq(acb_realref(b->coeffs+j),q,wp);
                    fmpq_poly_get_coeff_fmpq(q,coeff,1); arb_set_fmpq(acb_imagref(b->coeffs+j),q,wp);
                }
            }
            _acb_poly_set_length(b,f->length);
            gr_ctx_clear(A);
            slong isolated=acb_poly_find_roots(r,b,have_initial?r:nullptr,std::max(100L,4*n),wp);
            have_initial=true;
            for(slong j=0;j<n;++j) have_initial &= acb_is_finite(r+j);
            success=isolated==n;
            for(slong j=0;j<n;++j)
                success &= acb_is_finite(r+j) && (acb_is_zero(r+j) || acb_rel_accuracy_bits(r+j)>=bits);
            if(success) break;
        }
        if(!success) throw std::runtime_error("isolation/accuracy limit reached (32768 bits)");
        for(slong j=0;j<n;++j) for(slong m=0;m<mult;++m) {
            out.emplace_back(); acb_set(out.back().z,r+j);
        }
        _acb_vec_clear(r,n); acb_poly_clear(b);
    }
    gr_vec_clear(factors,P); gr_vec_clear(exponents,Z); gr_poly_clear(p,K);
    gr_heap_clear(c,K); gr_heap_clear(v,K); gr_heap_clear(unit,K); gr_heap_clear(leading,K);
    fmpq_clear(q); gr_ctx_clear(P); gr_ctx_clear(Z); gr_ctx_clear(K); gr_ctx_clear(Q);
    if (!real) nf_clear(nf);
    fmpq_poly_clear(modulus); fmpq_poly_clear(coeff);
    return out;
}
static std::vector<Ball> mps_roots(const std::vector<Coeff>& a,long bits,const std::string& kind,long inbits,int threads) {
    int n=a.size()-1;
    if(!n) return {};
    mps_context* s=mps_context_new();
    mps_context_set_n_threads(s,threads);
    mps_context_select_algorithm(s,MPS_ALGORITHM_SECULAR_GA);
    mps_monomial_poly* p=mps_monomial_poly_new(s,n);
    for(int j=0;j<=n;++j) {
        if(kind=="double") mps_monomial_poly_set_coefficient_d(s,p,j,a[j].re.get_d(),a[j].im.get_d());
        else if(kind=="mpfr") {
            mpc_t z; mpc_init2(z,inbits);
            mpf_set_q(mpc_Re(z),a[j].re.get_mpq_t()); mpf_set_q(mpc_Im(z),a[j].im.get_mpq_t());
            mps_monomial_poly_set_coefficient_f(s,p,j,z); mpc_clear(z);
        } else { auto re=a[j].re, im=a[j].im; mps_monomial_poly_set_coefficient_q(s,p,j,re.get_mpq_t(),im.get_mpq_t()); }
    }
    mps_context_set_input_poly(s,MPS_POLYNOMIAL(p));
    mps_context_set_output_prec(s,bits); mps_context_set_output_goal(s,MPS_OUTPUT_GOAL_APPROXIMATE);
    mps_mpsolve(s);
    if(mps_context_has_errors(s)) throw std::runtime_error("MPSolve reported an error");
    std::vector<Ball> out(n);
    if(bits<=53) {
        cplx_t* r=cplx_valloc(n); mps_context_get_roots_d(s,&r,nullptr);
        for(int j=0;j<n;++j) acb_set_d_d(out[j].z,cplx_Re(r[j]),cplx_Im(r[j]));
        free(r);
    } else {
        mpc_t* r=nullptr; rdpe_t* radii=nullptr; mps_context_get_roots_m(s,&r,&radii);
        mpfr_t x; mpfr_init2(x,bits);
        for(int j=0;j<n;++j) {
            mpfr_set_f(x,mpc_Re(r[j]),MPFR_RNDN); arb_set_interval_mpfr(acb_realref(out[j].z),x,x,bits);
            mpfr_set_f(x,mpc_Im(r[j]),MPFR_RNDN); arb_set_interval_mpfr(acb_imagref(out[j].z),x,x,bits);
            mpc_clear(r[j]);
        }
        mpfr_clear(x); free(r); free(radii);
    }
    mps_monomial_poly_free(s,(mps_polynomial*)p); mps_context_free(s);
    return out;
}
int main(int argc,char** argv) {
 try {
    if(argc!=4) throw std::runtime_error("usage: roots {flint|flint-target|mps} INPUT THREADS");
    const std::string backend=argv[1];
    if(backend!="flint" && backend!="flint-target" && backend!="mps") throw std::runtime_error("unknown backend");
    std::ifstream in(argv[2]); long n,bits,inbits; std::string kind;
    if(!(in>>n>>bits>>kind>>inbits)||n<0||bits<2) throw std::runtime_error("invalid input header");
    std::vector<Coeff> a(n+1);
    for(auto& c:a) {
        std::string re,im; if(!(in>>re>>im)) throw std::runtime_error("missing coefficient");
        auto parse=[&](const std::string& text) {
            if(text.find_first_of(".eE") == std::string::npos) return mpq_class(text);
            mpfr_t x; mpfr_init2(x,kind=="double"?53:inbits);
            if(mpfr_set_str(x,text.c_str(),10,MPFR_RNDN)) throw std::runtime_error("invalid decimal coefficient");
            mpq_class q; mpfr_get_q(q.get_mpq_t(),x); mpfr_clear(x); return q;
        };
        c.re=parse(re); c.im=parse(im); c.re.canonicalize(); c.im.canonicalize();
        if(kind!="exact") {roundq(c.re,kind=="double"?53:inbits); roundq(c.im,kind=="double"?53:inbits);}
    }
    while(a.size()>1&&a.back().re==0&&a.back().im==0) a.pop_back();
    if(a.size()==1&&a[0].re==0&&a[0].im==0) throw std::runtime_error("zero polynomial");
    flint_set_num_threads(std::stoi(argv[3]));
    double prep=0; long wp=0; std::vector<Ball> roots;
    std::vector<double> times;
    const char* count=std::getenv("M2_FLINT_ROOTS_TRIALS");
    int trials=count?std::stoi(count):4;
    if(trials<1) throw std::runtime_error("invalid trial count");
    for (int trial=0;trial<trials;++trial) {
        double start=seconds(); prep=start;
        roots=backend!="mps"?flint_roots(a,bits,prep,wp,backend=="flint"):mps_roots(a,bits,kind,inbits,std::stoi(argv[3]));
        if(trial || trials==1) times.push_back(seconds()-start);
    }
    std::sort(times.begin(),times.end()); double elapsed=times[times.size()/2];
    std::cout.precision(12);
    std::cout<<"time "<<elapsed<<" preprocess "<<(wp?prep:0)<<" workprec "<<wp<<" count "<<roots.size()<<"\n";
    mpfr_t x; mpfr_init2(x,bits);
    for(auto& r:roots) {
        arf_get_mpfr(x,arb_midref(acb_realref(r.z)),MPFR_RNDN); mpfr_out_str(stdout,10,0,x,MPFR_RNDN); std::cout<<" ";
        arf_get_mpfr(x,arb_midref(acb_imagref(r.z)),MPFR_RNDN); mpfr_out_str(stdout,10,0,x,MPFR_RNDN); std::cout<<" "<<acb_rel_accuracy_bits(r.z)<<"\n";
    }
    mpfr_clear(x);
 } catch(const std::exception& e) {std::cerr<<e.what()<<"\n";return 1;}
}
