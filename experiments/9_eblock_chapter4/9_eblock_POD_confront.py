from dolfin import *
from RBniCS import *
import matplotlib.pyplot as plt

class Eblock(EllipticCoercivePODBase):
    
    def __init__(self, V, subd, bound):
        bc_list = [
            DirichletBC(V, (0.0, 0.0), bound, 4),
            DirichletBC(V, (0.0, 0.0), bound, 5),
            DirichletBC(V, (0.0, 0.0), bound, 6),
            DirichletBC(V, (0.0, 0.0), bound, 10),
            DirichletBC(V, (0.0, 0.0), bound, 11),
            DirichletBC(V, (0.0, 0.0), bound, 12)
        ]
        super(Eblock, self).__init__(V, bc_list)
        self.dx = Measure("dx")(subdomain_data=subd)
        self.ds = Measure("ds")(subdomain_data=bound)
        self.f = Constant((1.0, 0.0))
        self.E  = 1.0
        self.nu = 0.3
        self.lambda_1 = self.E*self.nu / ((1.0 + self.nu)*(1.0 - 2.0*self.nu))
        self.lambda_2 = self.E / (2.0*(1.0 + self.nu))
        
    def compute_theta_a(self):
        mu = self.mu
        mu1 = mu[0]
        mu2 = mu[1]
        mu3 = mu[2]
        mu4 = mu[3]
        mu5 = mu[4]
        mu6 = mu[5]
        mu7 = mu[6]
        mu8 = mu[7]
        mu9 = mu[8]
        theta_a0 = mu1
        theta_a1 = mu2
        theta_a2 = mu3
        theta_a3 = mu4
        theta_a4 = mu5
        theta_a5 = mu6
        theta_a6 = mu7
        theta_a7 = mu8
        theta_a8 = mu9
        return (theta_a0, theta_a1 ,theta_a2 ,theta_a3 ,theta_a4 ,theta_a5 ,theta_a6 ,theta_a7 ,theta_a8)
    
    def compute_theta_f(self):
        mu = self.mu
        mu10 = mu[9]
        mu11 = mu[10]
        mu12 = mu[11]
        theta_f0 = mu10
        theta_f1 = mu11
        theta_f2 = mu12
        return (theta_f0, theta_f1, theta_f2)
    
    ## Set matrices resulting from the truth discretization of a.
    def assemble_truth_a(self):
        u = self.u
        v = self.v
        dx = self.dx
        # Define
        a0 = self.elasticity(u,v)*dx(1) +1e-15*inner(u,v)*dx
        a1 = self.elasticity(u,v)*dx(2) +1e-15*inner(u,v)*dx
        a2 = self.elasticity(u,v)*dx(3) +1e-15*inner(u,v)*dx
        a3 = self.elasticity(u,v)*dx(4) +1e-15*inner(u,v)*dx
        a4 = self.elasticity(u,v)*dx(5) +1e-15*inner(u,v)*dx
        a5 = self.elasticity(u,v)*dx(6) +1e-15*inner(u,v)*dx
        a6 = self.elasticity(u,v)*dx(7) +1e-15*inner(u,v)*dx
        a7 = self.elasticity(u,v)*dx(8) +1e-15*inner(u,v)*dx
        a8 = self.elasticity(u,v)*dx(9) +1e-15*inner(u,v)*dx
        # Assemble
        A0 = assemble(a0)
        A1 = assemble(a1)
        A2 = assemble(a2)
        A3 = assemble(a3)
        A4 = assemble(a4)
        A5 = assemble(a5)
        A6 = assemble(a6)
        A7 = assemble(a7)
        A8 = assemble(a8)
        # Return
        return (A0, A1, A2, A3, A4, A5, A6, A7, A8)
    
    ## Set vectors resulting from the truth discretization of f.
    def assemble_truth_f(self):
        v = self.v
        dx = self.dx
        ds = self.ds
        l = Constant((1e-11, 1e-11))
        f = self.f
        # Define
        f0 = inner(f,v)*ds(7) + inner(l,v)*dx
        f1 = inner(f,v)*ds(8) + inner(l,v)*dx 
        f2 = inner(f,v)*ds(9) + inner(l,v)*dx
        # Assemble
        F0 = assemble(f0)
        F1 = assemble(f1)
        F2 = assemble(f2)
        # Return
        return (F0,F1,F2)
    
    ## Auxiliary function to compute the elasticity bilinear form    
    def elasticity(self, u, v):
        lambda_1 = self.lambda_1
        lambda_2 = self.lambda_2
        return 2.0*lambda_2*inner(sym(grad(u)),sym(grad(v))) + lambda_1*tr(sym(grad(u)))*tr(sym(grad(v)))

#~~~~~~~~~~~~~~~~~~~~~~~~~     MAIN PROGRAM     ~~~~~~~~~~~~~~~~~~~~~~~~~# 

# 0.
Nmax = 10 
mean_error_u = np.zeros((Nmax,3))
mu_range = [(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0),(1.0, 3.0)]
first_mu = (1.5,2.0,2.5,1.5,2.0,2.5,1.5,2.0,2.5,1.5,2.0,2.5)

mesh = Mesh("Data/9_tblock.xml")
subd = MeshFunction("size_t", mesh, "Data/9_tblock_physical_region.xml")
bound = MeshFunction("size_t", mesh, "Data/9_tblock_facet_region.xml")

V = VectorFunctionSpace(mesh, "Lagrange", 1)

parameters.linear_algebra_backend = 'PETSc'

N_xi_train = 100
N_xi_test = 500

alpha = [(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.),(10.,10.)]
originalDistribution = BetaDistribution(alpha)
originalWeight = BetaWeight(alpha) 

# 1.0
eb_0 = Eblock(V, subd, bound)

eb_0.setmu_range(mu_range)
eb_0.setNmax(Nmax)

distribution = UniformDistribution()

eb_0.setxi_train(N_xi_train, sampling=distribution)
eb_0.set_weighted_flag(0)

eb_0.setmu(first_mu)
eb_0.offline() 

eb_0.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,0] = eb_0.error_analysis()

# 1.1
eb_1 = Eblock(V, subd, bound)

eb_1.setmu_range(mu_range)
eb_1.setNmax(Nmax)

distribution = originalDistribution

eb_1.setxi_train(N_xi_train, sampling=distribution)
eb_1.set_weighted_flag(0)

eb_1.setmu(first_mu)
eb_1.offline() 

eb_1.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,1] = eb_1.error_analysis()

# 1.2
eb_2 = Eblock(V, subd, bound)

eb_2.setmu_range(mu_range)
eb_2.setNmax(Nmax)

distribution = UniformDistribution()
density = originalWeight

eb_2.setxi_train(N_xi_train, sampling=distribution)
eb_2.set_density(weight=density)
eb_2.set_weighted_flag(1)

eb_2.setmu(first_mu)
eb_2.offline() 

eb_2.setxi_test(N_xi_test, enable_import=True, sampling=originalDistribution)
mean_error_u[:,2] = eb_2.error_analysis()

# 2. Plot the errors

plt.plot(np.log10(mean_error_u[:,0]),'b',label='POD - Uniform')
plt.plot(np.log10(mean_error_u[:,1]),'r',label='POD - Distribution')
plt.plot(np.log10(mean_error_u[:,2]),'k',label='Weighted POD - Uniform')
plt.legend()
plt.show()
