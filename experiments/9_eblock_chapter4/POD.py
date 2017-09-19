from dolfin import *
from RBniCS import *
import matplotlib.pyplot as plt

class Tblock(EllipticCoercivePODBase):

    def __init__(self, V, subd, bound):
        bc_list = [
            DirichletBC(V, 0.0, bound, 1),
            DirichletBC(V, 0.0, bound, 2),
            DirichletBC(V, 0.0, bound, 3),
            DirichletBC(V, 0.0, bound, 4),
            DirichletBC(V, 0.0, bound, 5),
            DirichletBC(V, 0.0, bound, 6),
            DirichletBC(V, 0.0, bound, 7),
            DirichletBC(V, 0.0, bound, 8),
            DirichletBC(V, 0.0, bound, 9),
            DirichletBC(V, 0.0, bound, 10),
            DirichletBC(V, 0.0, bound, 11),
            DirichletBC(V, 0.0, bound, 12)
        ]
        super(Tblock, self).__init__(V, bc_list)
        self.dx = Measure("dx")(subdomain_data=subd)
        self.ds = Measure("ds")(subdomain_data=bound)
        # Use the H^1 seminorm on V as norm, instead of the H^1 norm
        u = self.u
        v = self.v
        dx = self.dx
        scalar = inner(grad(u),grad(v))*dx
        self.S = assemble(scalar)
        [bc.apply(self.S) for bc in self.bc_list] # make sure to apply BCs to the inner product matrix
    
    ## Return the alpha_lower bound.
    def get_alpha_lb(self):
        return min(self.compute_theta_a())
    
    ## Set theta multiplicative terms of the affine expansion of a.
    def compute_theta_a(self):
        mu1 = self.mu[0]
    	mu2 = self.mu[1]
    	mu3 = self.mu[2]
    	mu4 = self.mu[3]
    	mu5 = self.mu[4]
    	mu6 = self.mu[5]
    	mu7 = self.mu[6]
    	mu8 = self.mu[7]
    	mu9 = self.mu[8]
        theta_a0 = mu1
        theta_a1 = mu2
    	theta_a2 = mu3
        theta_a3 = mu4
        theta_a4 = mu5
        theta_a5 = mu6
    	theta_a6 = mu7
        theta_a7 = mu8
        theta_a8 = mu9
        return (theta_a0, theta_a1, theta_a2, theta_a3, theta_a4, theta_a5, theta_a6, theta_a7, theta_a8)
    
    ## Set theta multiplicative terms of the affine expansion of f.
    def compute_theta_f(self):
        return (1.0,)
    
    ## Set matrices resulting from the truth discretization of a.
    def assemble_truth_a(self):
        u = self.u
        v = self.v
        dx = self.dx
        # Assemble A0
        a0 = inner(grad(u),grad(v))*dx(1) + 1e-15*inner(u,v)*dx
        A0 = assemble(a0)
        # Assemble A1
        a1 = inner(grad(u),grad(v))*dx(2) + 1e-15*inner(u,v)*dx
        A1 = assemble(a1)
    	# Assemble A2
        a2 = inner(grad(u),grad(v))*dx(3) + 1e-15*inner(u,v)*dx
        A2 = assemble(a2)
        # Assemble A3
        a3 = inner(grad(u),grad(v))*dx(4) + 1e-15*inner(u,v)*dx
        A3 = assemble(a3)
        # Assemble A4
        a4 = inner(grad(u),grad(v))*dx(5) + 1e-15*inner(u,v)*dx
        A4 = assemble(a4)
        # Assemble A5
        a5 = inner(grad(u),grad(v))*dx(6) + 1e-15*inner(u,v)*dx
        A5 = assemble(a5)
    	# Assemble A6
        a6 = inner(grad(u),grad(v))*dx(7) + 1e-15*inner(u,v)*dx
        A6 = assemble(a6)
        # Assemble A7
        a7 = inner(grad(u),grad(v))*dx(8) + 1e-15*inner(u,v)*dx
        A7 = assemble(a7)
        # Assemble A8
        a8 = inner(grad(u),grad(v))*dx(9) + 1e-15*inner(u,v)*dx
        A8 = assemble(a8)
        # Return
        return (A0, A1, A2, A3, A4, A5, A6, A7, A8)
    
    ## Set vectors resulting from the truth discretization of f.
    def assemble_truth_f(self):
        v = self.v
        dx = self.dx
        ds = self.ds
        # Assemble F0
        f0 = v*dx
        F0 = assemble(f0)
        # Return
        return (F0,)

#~~~~~~~~~~~~~~~~~~~~~~~~~     MAIN PROGRAM     ~~~~~~~~~~~~~~~~~~~~~~~~~# 

# 0.

Nmax = 15
mean_error_u = np.zeros((Nmax,6))
mu_range = [(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0)]

mesh = Mesh("Data/9_tblock.xml")
subd = MeshFunction("size_t", mesh, "Data/9_tblock_physical_region.xml")
bound = MeshFunction("size_t", mesh, "Data/9_tblock_facet_region.xml")

V = FunctionSpace(mesh, "Lagrange", 1)

parameters.linear_algebra_backend = 'PETSc'

N_xi_train = 500
N_xi_test = 500

param = [(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.)]
Qparam = [(9.,9.),(9.,9.),(9.,9.),(9.,9.),(9.,9.),(9.,9.),(9.,9.),(9.,9.),(9.,9.)]
originalDistribution = BetaDistribution(param)
originalWeight = BetaWeight(param) 
'''
# 1.0
tb_0 = Tblock(V, subd, bound)

tb_0.setmu_range(mu_range)
tb_0.setNmax(Nmax)

distribution = UniformDistribution()

tb_0.setxi_train(N_xi_train, sampling=distribution)
tb_0.set_weighted_flag(0)

tb_0.offline() 

tb_0.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,0] = tb_0.error_analysis()
'''
# 1.1
tb_1 = Tblock(V, subd, bound)

tb_1.setmu_range(mu_range)
tb_1.setNmax(Nmax)

distribution = originalDistribution

tb_1.setxi_train(N_xi_train, sampling=distribution)
tb_1.set_weighted_flag(0)

tb_1.offline() 

tb_1.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,1] = tb_1.error_analysis()

# 1.2
tb_2 = Tblock(V, subd, bound)

tb_2.setmu_range(mu_range)
tb_2.setNmax(Nmax)

distribution = UniformDistribution()
density = originalWeight

tb_2.setxi_train(2000, sampling=distribution)
tb_2.set_density(weight=density)
tb_2.set_weighted_flag(1)

tb_2.offline() 

tb_2.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,2] = tb_2.error_analysis()
'''
# 1.3
tb_3 = Tblock(V, subd, bound)

tb_3.setmu_range(mu_range)
tb_3.setNmax(Nmax)

distribution = QuadratureDistribution('GaussJacobi',1)
density = QuadratureWeight(IndicatorWeight(originalWeight,0.),'GaussJacobi',1,alpha=Qparam)

tb_3.setxi_train(500, sampling=distribution)
tb_3.set_density(weight=density)
tb_3.set_weighted_flag(1)

tb_3.offline() 

tb_3.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,3] = tb_3.error_analysis()

# 1.4
tb_4 = Tblock(V, subd, bound)
tb_4.setmu_range(mu_range)
tb_4.setNmax(Nmax)

distribution = QuadratureDistribution('GaussJacobi',0)
density = QuadratureWeight(IndicatorWeight(originalWeight,0.),'GaussJacobi',0,alpha=Qparam)

tb_4.setxi_train(N_xi_train, sampling=distribution)
tb_4.set_density(weight=density)
tb_4.set_weighted_flag(1)

tb_4.offline() 

tb_4.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,4] = tb_4.error_analysis()

# 1.5
tb_5 = Tblock(V, subd, bound)

tb_5.setmu_range(mu_range)
tb_5.setNmax(Nmax)

distribution = QuadratureDistribution('GaussJacobi',0,alpha=param)
density = QuadratureWeight(IndicatorWeight(originalWeight,0.),'GaussJacobi',0,alpha=Qparam)

tb_5.setxi_train(N_xi_train, sampling=distribution)
tb_5.set_density(weight=density)
tb_5.set_weighted_flag(1)

tb_5.offline() 

tb_5.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,5] = tb_5.error_analysis()
'''
# 7. Plot the errors

#plt.plot(np.log10(mean_error_u[:,0]),'r',label='Standard POD')
plt.plot(np.log10(mean_error_u[:,1]),'b-o',label='Monte-Carlo POD')
plt.plot(np.log10(mean_error_u[:,2]),'y-*',label='Uniform Monte-Carlo POD')
#plt.plot(np.log10(mean_error_u[:,3]),'y',label='POD - GaussLegendre Sparse')
#plt.plot(np.log10(mean_error_u[:,4]),'k',label='POD - GaussLegendre')
#plt.plot(np.log10(mean_error_u[:,5]),'g',label='POD - GaussJacobi')
plt.title('error comparison: first trial')
#plt.title('error comparison: second trial')
plt.xlabel('$N$')
plt.ylabel('$\log_{10}(E[\parallel u_{N_\delta}(Y)-u_N(Y)\parallel_{H^1_0(\Omega)}^2])$')
plt.legend()
plt.show()

# 8. Returns the best method #
'''
mean_N_err = np.mean(np.log10(mean_error_u), axis=0) #
m = min(mean_N_err) #
print [i for i in range(6) if mean_N_err[i] == m] #
for i in range(6): #
    sampling_cardinality = 'len(tb_'+str(i)+'.xi_train)' #
    print eval(sampling_cardinality) #
'''