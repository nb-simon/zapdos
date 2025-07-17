# test file

## naming conventions
# em: electrons
# D: deuterium atoms
# Dp: deuterium atomic ions
# D2: deuterium molecules
# D2p: deuterium molecular ions
# Tp: tritium atomic ions
# He3: helium 3 atomic ions (fully ionized)
# He4: helium 4 atomic ions (fully ionized)
# nt: neutrons
# pt: protons

# file/kernel structure influenced by ad_argon.i and townsend_units.i from Zapdos tests

dom0Scale = 1e-3
dom1Scale = 1e-7

[GlobalParams]
    offset = 20 # chosen arbitrarily, taken from townsend_units.i
    potential_units = kV
    use_moles = true
[]

[Mesh]
    [file]
        type = FileMeshGenerator # reads mesh file
        file = '?' # will need to change when I get a mesh file
    []
    [interface] # I don't know what the rest of these blocks do, stolen from townsend_units.i
        type = SideSetsBetweenSubdomainsGenerator # MeshGenerator that creates a sideset composed of the nodes located between two or more subdomains
        primary_block = '0'
        paired_block = '1'
        new_boundary = 'master0_interface'
        input = file
    []
    [interface_again]
        type = SideSetsBetweenSubdomainsGenerator
        primary_block = '1'
        paired_block = '0'
        new_boundary = 'master1_interface'
        input = interface
    []
    [left]
        type = SideSetsFromNormalsGenerator # Adds a new named sideset to the mesh for all faces matching the specified normal
        normals = '-1 0 0'
        new_boundary = 'left'
        input = interface_again
    []
    [right]
        type = SideSetsFromNormalsGenerator
        normals = '1 0 0'
        new_boundary = 'right'
        input = left
    []
[]

[Problem]
    type = FEProblem # A normal (default) Problem object that contains a single NonlinearSystem and a single AuxiliarySystem object
[]

[Preconditioning]
    [smp]
        type = SMP # Single matrix preconditioner (SMP) builds a preconditioner using user defined off-diagonal parts of the Jacobian
        full = true
    []
[]

[Executioner]
    type = Transient # Executioner for time varying simulations
    automatic_scaling = true
    compute_scaling_once = false # this and preceeding setting are in ad_argon.i, but not townsend_units.i, don't know what they do
    end_time = 1e-1
    petsc_options = '-snes_converged_reason -snes_linesearch_monitor'
    solve_type = NEWTON
    line_search = 'basic'
    petsc_options_iname = '-pc_type -pc_factor_shift_type -pc_factor_shift_amount'
    petsc_options_value = 'lu NONZERO 1.e-10'
    nl_rel_tol = 1e-4 # this and next 3 values may need to change, stolen from townsend_units.i
    nl_abs_tol = 7.6e-5
    dtmin = 1e-15
    l_max_its = 20
    [TimeSteppers]
        [Adaptive]
            type = IterationAdaptiveDT # Adjust the timestep based on the number of iterations
            cutback_factor = 0.4
            dt = 1e-11
            growth_factor = 1.2
            optimal_iterations = 30
        []
    []
[]

[Outputs]
    perf_graph = true
    [out]
        type = Exodus # Object for output data in the Exodus format
        execute_on = 'final'
    []
[]

[Debug]
    show_var_residual_norms = true # this was commented out in townsend_units.i
[]

[UserObjects]
    [data_provider] # not really sure how much of this block is necessary for this problem
        type = ProvideMobility # Defines ballast resistance and the area of an electrode(Used with Circuit BCs)
        electrode_area = 5.02e-7 # copied arbitrary value, likely will not need in this application
        ballast_resist = 1e6 # don't know what this value is
        e = 1.6e-19
    []
[]

# KERNELS, AUXKERNELS, VARIABLES, AND AUXVARIABLES WILL NEED TO CHANGE FOR PROBLEM
[Kernels]
    [em_time_deriv]
        type = ElectronTimeDerivative # Generic accumulation term for variables in logarithmic form
        variable = em
        block = 0
    []
    [em_advection]
        type = EFieldAdvection # The discontinuous Galerkin form of the generic electric field driven advection term(Densities must be in log form)
        variable = em
        block = 0
        position_units = ${dom0Scale}
    []
    [em_diffusion]
        type = CoeffDiffusion # Generic diffusion term (densities must be in logarithmic form), where the Jacobian is computed using forward automatic differentiation
        variable = em
        block = 0
        position_units = ${dom0Scale}
    []
    [em_log_stabilization]
        type = LogStabilizationMoles # Kernel stabilizes solution variable u in places where u → 0; b is the offset valuespecified by the user. A typical value for b is 20
        variable = em
        block = 0
    []

    [potential_diffusion_dom1]
        type = CoeffDiffusionLin # Generic linear diffusion term (Values are NOT in logarithmic form), where the Jacobian is computed using forward automatic differentiation
        variable = potential
        block = 0
        position units = ${dom0Scale}
    []
    [potential_diffusion_dom2]
        type = CoeffDiffusionLin
        variable = potential
        block = 1
        position units = ${dom1Scale}
    []

    [Dp_charge_source]
        type = ChargeSourceMoles_KV # Used for adding charged sources to Poisson’s equation. This kernel assumes that densities are measured in units of mol/m^3 as opposed to #/m^3
        variable = potential
        charged = Dp
        block = 0
    []
    [D2p_charge_source]
        type = ChargeSourceMoles_KV
        variable = potential
        charged = D2p
        block = 0
    []
    [Tp_charge_source]
        type = ChargeSourceMoles_KV
        variable = potential
        charged = Tp
        block = 0
    []
    [He3_charge_source]
        type = ChargeSourceMoles_KV
        variable = potential
        charged = He3
        block = 0
    []
    [He4_charge_source]
        type = ChargeSourceMoles_KV
        variable = potential
        charged = He4
        block = 0
    []
    [em_charge_source]
        type = ChargeSourceMoles_KV
        variable = potential
        charged = em
        block = 0
    []

    [Dp_time_deriv]
        type = ElectronTimeDerivative
        variable = Dp
        block = 0
    []
    [Dp_advection]
        type = EFieldAdvection
        variable = Dp
        block = 0
        position_units = ${dom0Scale}
    []
    [Dp_diffusion]
        type = CoeffDiffusion
        variable = Dp
        block = 0
        position_units = ${dom0Scale}
    []
    [Dp_log_stabilization]
        type = LogStabilizationMoles
        variable = Dp
        block = 0
    []

    [D2p_time_deriv]
        type = ElectronTimeDerivative
        variable = D2p
        block = 0
    []
    [D2p_advection]
        type = EFieldAdvection
        variable = D2p
        block = 0
        position_units = ${dom0Scale}
    []
    [D2p_diffusion]
        type = CoeffDiffusion
        variable = D2p
        block = 0
        position_units = ${dom0Scale}
    []
    [D2p_log_stabilization]
        type = LogStabilizationMoles
        variable = D2p
        block = 0
    []

    [Tp_time_deriv]
        type = ElectronTimeDerivative
        variable = Tp
        block = 0
    []
    [Tp_advection]
        type = EFieldAdvection
        variable = Tp
        block = 0
        position_units = ${dom0Scale}
    []
    [Tp_diffusion]
        type = CoeffDiffusion
        variable = Tp
        block = 0
        position_units = ${dom0Scale}
    []
    [Tp_log_stabilization]
        type = LogStabilizationMoles
        variable = Tp
        block = 0
    []

    [He3_time_deriv]
        type = ElectronTimeDerivative
        variable = He3
        block = 0
    []
    [He3_advection]
        type = EFieldAdvection
        variable = He3
        block = 0
        position_units = ${dom0Scale}
    []
    [He3_diffusion]
        type = CoeffDiffusion
        variable = He3
        block = 0
        position_units = ${dom0Scale}
    []
    [He3_log_stabilization]
        type = LogStabilizationMoles
        variable = He3
        block = 0
    []

    [He4_time_deriv]
        type = ElectronTimeDerivative
        variable = He4
        block = 0
    []
    [He4_advection]
        type = EFieldAdvection
        variable = He4
        block = 0
        position_units = ${dom0Scale}
    []
    [He4_diffusion]
        type = CoeffDiffusion
        variable = He4
        block = 0
        position_units = ${dom0Scale}
    []
    [He4_log_stabilization]
        type = LogStabilizationMoles
        variable = He4
        block = 0
    []

    [mean_en_time_deriv]
        type = ElectronTimeDerivative
        variable = mean_en
        block = 0
    []
    [mean_en_advection]
        type = EFieldAdvection
        block = 0
        position_units = ${dom0Scale}
    []
    [mean_en_diffusion]
        type = CoeffDiffusion
        variable = mean_en
        block = 0
        position_units = ${dom0Scale}
    []
    [mean_en_joule_heating]
        type = JouleHeating # Joule heating term for electrons (densities must be in logarithmic form), where the Jacobian is computed using forward automatic differentiation
        variable = mean_en
        em = em
        block = 0
        position_units = ${dom0Scale}
    []
    [mean_en_log_stabilization]
        type = LogStabilizationMoles
        variable = mean_en
        block = 0
        offset = 15
    []
[]

[Variables]
    [potential]
    []

    [em]
        block = 0
    []
    
    [Dp]
        block = 0
    []

    [D2p]
        block = 0
    []

    [D]
        block = 0
    []

    [Tp]
        block = 0
    []

    [He3]
        block = 0
    []

    [He4]
        block = 0
    []

    [mean_en]
        block = 0
    []
[]

[AuxVariables]
    [D2]
        block = 0
        order = CONSTANT
        family = MONOMIAL
        initial_condition = ? # CHECK
    []
    [e_temp]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [x]
        order = CONSTANT
        family = MONOMIAL
    []
    [x_node]
    []
    [em_lin] # I don't know what these _lin auxvariables do, but I (might've) made the relevant versions
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [Dp_lin]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [D2p_lin]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [D_lin]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [Tp_lin]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [He3_lin]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [He4_lin]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [Efield]
        order = CONSTANT
        family = MONOMIAL
    []
    [Current_em]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [Current_Dp]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [Current_D2p]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [Current_Tp]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [Current_He3]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [Current_He4]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    #[Current_D] # commented out b/c not an ion
    #    block = 0
    #    order = CONSTANT
    #    family = MONOMIAL
    #[]
    [tot_gas_current]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [EFieldAdvAux_em]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [DiffusiveFlux_em]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [PowerDep_em]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [PowerDep_Dp]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [PowerDep_D2p]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [PowerDep_Tp]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [PowerDep_He3]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [PowerDep_He4]
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
    [PowerDep_D] # might not need this one b/c it's not an ion?
        block = 0
        order = CONSTANT
        family = MONOMIAL
    []
[]

[AuxKernels]
    [PowerDep_em]
        type = ADPowerDep # Amount of power deposited into a user specified specie by Joule Heating
        density_log = em
        art_diff = false
        potential_units = kV
        variable = PowerDep_em
        position_units = ${dom0Scale}
        block = 0
    []
    [PowerDep_Dp]
        type = ADPowerDep
        density_log = Dp
        art_diff = false
        potential_units = kV
        variable = PowerDep_Dp
        position_units = ${dom0Scale}
        block = 0
    []
    [PowerDep_D2p]
        type = ADPowerDep
        density_log = D2p
        art_diff = false
        potential_units = kV
        variable = PowerDep_D2p
        position_units = ${dom0Scale}
        block = 0
    []
    [PowerDep_Tp]
        type = ADPowerDep
        density_log = Tp
        art_diff = false
        potential_units = kV
        variable = PowerDep_Tp
        position_units = ${dom0Scale}
        block = 0
    []
    [PowerDep_He3]
        type = ADPowerDep
        density_log = He3
        art_diff = false
        potential_units = kV
        variable = PowerDep_He3
        position_units = ${dom0Scale}
        block = 0
    []
    [PowerDep_He4]
        type = ADPowerDep
        density_log = He4
        art_diff = false
        potential_units = kV
        variable = PowerDep_He4
        position_units = ${dom0Scale}
        block = 0
    []
    [PowerDep_D] # like above, might not need b/c not an ion
        type = ADPowerDep
        density_log = D
        art_diff = false
        potential_units = kV
        variable = PowerDep_D
        position_units = ${dom0Scale}
        block = 0
    []
    [e_temp]
        type = ElectronTemperature # Returns the electron temperature
        variable = e_temp
        electron_density = em
        mean_en = mean_en
        block = 0
    []
    [x_g]
        type = Position # Produces an elemental auxiliary variable useful for plotting against other elemental auxiliary variables. Mesh points automatically output by Zapdos only work for plotting nodal variables. Since almost all auxiliary variables are elemental, this AuxKernel is very important
        variable = x
        position_units = ${dom0Scale}
        block = 0
    []
    #[x_l] # commented b/c from liquid
    #    type = Position
    #    variable = x
    #    position_units = ${dom1Scale}
    #    block = 1
    #[]
    [x_ng]
        type = Position
        variable = x_node
        position_units = ${dom0Scale}
        block = 0
    []
    #[x_nl] # commented b/c from liquid
    #    type = Position
    #    variable = x_node
    #    position_units = ${dom1Scale}
    #    block = 1
    #[]
    [tot_gas_current]
        type = ParsedAux # Sets a field variable value to the evaluation of a parsed expression
        variable = tot_gas_current
        coupled_variables = 'Current_em Current_Arp'
        expression = 'Current_em + Current_Arp'
        execute_on = 'timestep_end'
        block = 0
    []
    [em_lin]
        type = DensityMoles # Returns physical densities in units of #/m^3
        variable = em_lin
        density_log = emblock = 0
    []
    [Dp_lin]
        type = DensityMoles
        variable = Dp_lin
        density_log = Dp
        block = 0
    []
    [D2p_lin]
        type = DensityMoles
        variable = D2p_lin
        density_log = D2p
        block = 0
    []
    [Tp_lin]
        type = DensityMoles
        variable = Tp_lin
        density_log = Tp
        block = 0
    []
    [He3_lin]
        type = DensityMoles
        variable = He3_lin
        density_log = He3
        block = 0
    []
    [He4_lin]
        type = DensityMoles
        variable = He4_lin
        density_log = He4
        block = 0
    []
    [D_lin]
        type = DensityMoles
        variable = D_lin
        density_log = D
        block = 0
    []
    [Efield_g]
        type = Efield # Returns the defined component of the electric field (0 = x, 1 = y, 2 = z)
        component = 0
        variable = Efield
        position_units = ${dom0Scale}
        block = 0
    []
    #[Efield_l] # commented b/c from liquid
    #    type = Efield
    #    component = 0
    #    variable = Efield
    #    position_units = ${dom1Scale}
    #    block = 1
    #[]
    [Current_em]
        type = ADCurrent # Returns the electric current associated with the flux of the specified species
        density_log = em
        variable = Current_em
        art_diff = false
        position_units = ${dom0Scale}
        block = 0
    []
    [Current_Dp]
        type = ADCurrent
        density_log = Dp
        variable = Current_Dp
        art_diff = false
        position_units = ${dom0Scale}
        block = 0
    []
    [Current_D2p]
        type = ADCurrent
        density_log = D2p
        variable = Current_D2p
        art_diff = false
        position_units = ${dom0Scale}
        block = 0
    []
    [Current_Tp]
        type = ADCurrent
        density_log = Tp
        variable = Current_Tp
        art_diff = false
        position_units = ${dom0Scale}
        block = 0
    []
    [Current_He3]
        type = ADCurrent
        density_log = He3
        variable = Current_He3
        art_diff = false
        position_units = ${dom0Scale}
        block = 0
    []
    [Current_He4]
        type = ADCurrent
        density_log = He4
        variable = Current_He4
        art_diff = false
        position_units = ${dom0Scale}
        block = 0
    []
    #[Current_D] # commented b/c neutral particle so no associated ELECTRIC current
    #    type = ADCurrent
    #    density_log = D
    #    variable = Current_D
    #    art_diff = false
    #    position_units = ${dom0Scale}
    #    block = 0
    #[]
    [EFieldAdvAux_em]
        type = ADEFieldAdvAux # Returns the electric field driven advective flux of the specified species
        density_log = em
        variable = EFieldAdvAux_em
        position_units = ${dom0Scale}
        block = 0
    []
    [DiffusiveFlux_em]
        type = ADDiffusiveFlux
        density_log = em
        variable = DiffusiveFlux_em
        position_units = ${dom0Scale}
        block = 0
    []
[]


[InterfaceKernels] # used for plasma/water interface (?) for townsend_units.i
    [em_advection]
        type = InterfaceAdvection # Used to include the electric field driven advective flux of a species into or out of a neighboring subdomain
        neighbor_var = em
        variable = emliq
        boundary = master1_interface
        position_units = ${dom1Scale}
        neighbor_position_units = ${dom0Scale}
    []
    [em_diffusion]
        type = InterfaceLogDiffusionElectrons # Used to include the diffusive flux of species into or out of a neighboringsubdomain. Currently specific to electrons
        neighbor_var = em
        variable = emliq
        boundary = master1_interface
        position_units = ${dom1Scale}
        neighbor_position_units = ${dom0Scale}
    []
[]


[BCs]
    [mean_en_physical_right]
        type = HagelaarEnergyBC # Kinetic electron mean energy boundary condition
        varaible = mean_en
        boundary = 'master0_interface'
        electrons = em
        r = 0.99
        position_units = ${dom0Scale}
    []
    [mean_en_physical_left]
        type = HagelaarEnergyBC
        varaible = mean_en
        boundary = 'left'
        electrons = em
        r = 0
        position_units = ${dom0Scale}
    []
    [secondary_energy_left]
        type = SecondaryElectronEnergyBC # Kinetic secondary electron for mean electron energy boundary condition
        variable = mean_en
        boundary = 'left'
        electrons = em
        ions = 'Arp'
        r = 0
        emission_coeffs = 0.05
        secondary_electron_energy = 3
        position_units = ${dom0Scale}
    []
    [potential_left]
        type = NeumannCircuitVoltageMoles_KV # A Neumann boundary condition based on Kirchhoff's law of voltage
        variable = potential
        boundary = left
        function = potential_bc_func
        ions = Arp
        data_provider = data_provider
        electrons = em
        electron_energy = mean_en
        r = 0
        emission_coeffs = 0.05
        position_units = ${dom0Scale}
    []
    [potential_dirichlet_right]
        type = DirichletBC # Imposes the essential boundary condition u = g, where g is a constant, controllable value
        variable = potential
        boundary = right
        value = 0
    []
    [em_physical_right]
        type = HagelaarElectronBC # Kinetic electron boundary condition
        variable = em
        boundary = 'master0_interface'
        electron_energy = mean_en
        r = 0.99
        position_units = ${dom0Scale}
    []
    
    [Dp_physical_right_diffusion]
        type = HagelaarIonDiffusionBC # Kinetic ion boundary condition
        variable = Dp
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []
    [Dp_physical_right_advection]
        type = HagelaarIonAdvectionBC # Kinetic advective ion boundary condition
        variable = Dp
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []

    [D2p_physical_right_diffusion]
        type = HagelaarIonDiffusionBC
        variable = D2p
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []
    [D2p_physical_right_advection]
        type = HagelaarIonAdvectionBC
        variable = D2p
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []

    [Tp_physical_right_diffusion]
        type = HagelaarIonDiffusionBC
        variable = Tp
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []
    [Tp_physical_right_advection]
        type = HagelaarIonAdvectionBC
        variable = Tp
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []

    [He3_physical_right_diffusion]
        type = HagelaarIonDiffusionBC
        variable = He3
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []
    [He3_physical_right_advection]
        type = HagelaarIonAdvectionBC
        variable = He3
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []
    
    [He4_physical_right_diffusion]
        type = HagelaarIonDiffusionBC
        variable = He4
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []
    [He4_physical_right_advection]
        type = HagelaarIonAdvectionBC
        variable = He4
        boundary = 'master0_interface'
        r = 0
        position_units = ${dom0Scale}
    []

    [em_physical_left]
        type = HagelaarElectronBC
        variable = em
        boundary = 'left'
        electron_energy = mean_en
        r = 0
        position_units = ${dom0Scale}
    []
    [sec_electrons_left]
        type = SecondaryElectronBC # Kinetic secondary electron boundary condition
        variable = em
        boundary = 'left'
        ions = 'Arp'
        electron_energy = mean_en
        r = 0
        emission_coeffs = 0.05
        position_units = ${dom0Scale}
    []
    
    [Dp_physical_left_diffusion]
        type = HagelaarIonDiffusionBC
        variable = Dp
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []
    [Dp_physical_left_advection]
        type = HagelaarIonAdvectionBC
        variable = Dp
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []

    [D2p_physical_left_diffusion]
        type = HagelaarIonDiffusionBC
        variable = D2p
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []
    [D2p_physical_left_advection]
        type = HagelaarIonAdvectionBC
        variable = D2p
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []

    [Tp_physical_left_diffusion]
        type = HagelaarIonDiffusionBC
        variable = Tp
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []
    [Tp_physical_left_advection]
        type = HagelaarIonAdvectionBC
        variable = Tp
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []

    [He3_physical_left_diffusion]
        type = HagelaarIonDiffusionBC
        variable = He3
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []
    [He3_physical_left_advection]
        type = HagelaarIonAdvectionBC
        variable = He3
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []
    
    [He4_physical_left_diffusion]
        type = HagelaarIonDiffusionBC
        variable = He4
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []
    [He4_physical_left_advection]
        type = HagelaarIonAdvectionBC
        variable = He4
        boundary = 'left'
        r = 0
        position_units = ${dom0Scale}
    []
[]

[ICs]
    [em_ic]
        type = ConstantIC # Sets a constant field value
        variable = em
        value = -21
        block = 0
    []
    [Dp_ic]
        type = ConstantIC
        variable = Dp
        value = -21
        block = 0
    []
    [D2p_ic]
        type = ConstantIC
        variable = D2p
        value = -21
        block = 0
    []
    [Tp_ic]
        type = ConstantIC
        variable = Tp
        value = -21
        block = 0
    []
    [He3_ic]
        type = ConstantIC
        variable = He3
        value = -21
        block = 0
    []
    [He4_ic]
        type = ConstantIC
        variable = He4
        value = -21
        block = 0
    []
    [D_ic]
        type = ConstantIC
        variable = D
        value = -21
        block = 0
    []
    [mean_en_ic]
        type = ConstantIC
        variable = mean_en
        value = -20
        block = 0
    []
    [potential_ic]
        type = FunctionIC # An initial condition that uses a normal function of x, y, z to produce values (and optionally gradients) for a field variable
        variable = potential
        function = potential_ic_func
    []
[]

[Functions]
    [potential_bc_func]
        type = ParsedFunction # Function created by parsing a string
        expression = -1.25
    []
    [potential_ic_func]
        type = ParsedFunction
        expression = '-1.25 * (1.001e-3 - x)'
    []
[]

[Materials] # be careful with values in this block, currently borrowed from townsend_units.i
    [field_solver]
        type = FieldSolverMaterial # FieldSolverMaterial provides an electric field property for Zapdos objects. This enables an interface to an external electromagnetic field solver for all Zapdos objects. Default is an electrostatic interface, where the potential coupled variable parameter must be provided
        potential = potential
    []

    [test]
        type = GasElectronMoments # Material properties of electrons(Defines reaction properties with rate coefficients)
        interp_trans_coeffs = true
        interp_elastic_coeff = true
        ramp_trans_coeffs = false
        user_p_gas = 101325
        user_se_coeff = 0.05
        em = em
        mean_en = mean_en
        block = 0
        property_tables_file = ? # CHECK LATER
    []

    [test_block1]
        type = GenericConstantMaterial # Declares material properties based on names and values prescribed by input parameters
        block = 1
        prop_names = 'T_gas p_gas'
        prop values = 300 1.01e5'
    []

    [gas_species_0]
        type = ADHeavySpecies # Material properties of ions
        heavy_species_name = D
        heavy_species_mass = 3.34e-27
        heavy_species_charge = 0
        block = 0
    []

    [gas_species_1]
        type = ADHeavySpecies
        heavy_species_name = Dp
        heavy_species_mass = 3.34e-27
        heavy_species_charge = 1.0
        block = 0
    []

    [gas_species_2]
        type = ADHeavySpecies
        heavy_species_name = D2
        heavy_species_mass = 6.68e-27
        heavy_species_charge = 0
        block = 0
    []

    [gas_species_3]
        type = ADHeavySpecies
        heavy_species_name = D2p
        heavy_species_mass = 6.68e-27
        heavy_species_charge = 1.0
        block = 0
    []

    [gas_species_4]
        type = ADHeavySpecies
        heavy_species_name = Tp
        heavy_species_mass = 5.01e-27
        heavy_species_charge = 1.0
        block = 0
    []

    [gas_species_5]
        type = ADHeavySpecies
        heavy_species_name = He3
        heavy_species_mass = 5.01e-27
        heavy_species_charge = 1.0
        block = 0
    []

    [gas_species_6]
        type = ADHeavySpecies
        heavy_species_name = He4
        heavy_species_mass = 6.68e-27
        heavy_species_charge = 1.0
        block = 0
    []
[]

[Reactions]
    [Deuterium]
        species = 'em D Dp D2p'
        aux_species = 'D2'
        reaction_coefficient_format = 'rate' # this should probably be rate not townsend
        gas_species = 'D2'
        electron_energy = 'mean_en'
        electron_density = 'em'
        include_electrons = true
        file_location = ?
        potential = 'potential'
        use_log = true
        use_ad = true
        position_units = ${dom0Scale}
        track_rates = false
        block = 0

        reactions = 'em + D -> em + em + Dp         : 
                     em + D2 -> em + em + D2p       : 
                     em + D2p -> em + em + Dp + Dp  : 
                     em + D2 -> em + D + D          : 
                     em + D2 -> em + em + D + Dp    : 
                     em + D2p -> em + D + Dp        : 
                     em + D2p -> D + D2             : 
                     Dp + D -> D + Dp               : 
                     Dp + D2 -> D + D2p             : 
                     Dp + D2 -> Dp + D2             : 
                     Dp + em -> D                   : '

    []
[]





# fusion reactions
# may be able to neglect reactions with secondary species (e.g. He isotopes)
# don't know if I need to track neutrons/protons
                     Dp + Dp -> Tp + pt             :
                     Dp + Dp -> He3 + nt            :
                     Dp + Tp -> He4 + nt            :
                     Dp + He3 -> He4 + pt           :
                     Tp + Tp -> He4 + nt + nt       :
                     He3 + Tp -> He4 + pt + nt      :
                     He3 + Tp -> He4 + Dp           :
                     He3 + Tp -> He5 + pt           :