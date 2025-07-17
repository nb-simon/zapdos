#Testing implementation of simple fusion reactions at the pedestal
#Assumptions:
# temperature = 0.5 keV

[GlobalParams]
  potential_units = V
  use_moles = true
[]

[Mesh]
  #Sets up a 0D mesh with 1 element
  [geo]
    type = GeneratedMeshGenerator
    nx = 1
    dim = 1
  []
[]

#Defines the problem type, such as FE, eigen value problem, etc.
[Problem]
  type = FEProblem
[]

#User defined name for the variables.
#Other variable properties are defined here,
# such as family of shape function and variable order
# (the default family/order is Lagrange/First)
[Variables]
  #Main species densities in log-molar
  [Dp]
  []
  [em]
  []
  [D]
  []
  #[D2]
  #[]
  [D2p]
  []
[]

[AuxVariables]
  #Converted densities
  [Dp_density]
    order = CONSTANT
    family = MONOMIAL
  []
  [em_density]
    order = CONSTANT
    family = MONOMIAL
  []
  [D_density]
    order = CONSTANT
    family = MONOMIAL
  []
  [D2_density]
    order = CONSTANT
    family = MONOMIAL
  []
  [D2p_density]
    order = CONSTANT
    family = MONOMIAL
  []

  #D2 background gas
  [D2]
  []

  #Reaction rates
  [REI1]
    order = CONSTANT
    family = MONOMIAL
  []
  [REI2]
    order = CONSTANT
    family = MONOMIAL
  []
  [REI3]
    order = CONSTANT
    family = MONOMIAL
  []
  [RDS1]
    order = CONSTANT
    family = MONOMIAL
  []
  [RDS2]
    order = CONSTANT
    family = MONOMIAL
  []
  [RDS3]
    order = CONSTANT
    family = MONOMIAL
  []
  [RDS4]
    order = CONSTANT
    family = MONOMIAL
  []
  [RRC]
    order = CONSTANT
    family = MONOMIAL
  []
[]

[Kernels]
  #Adds the time derivative for the variables
  [dDp_dt]
    type = TimeDerivative
    variable = Dp
  []
  [dem_dt]
    type = TimeDerivative
    variable = em
  []
  [dD_dt]
    type = TimeDerivative
    variable = D
  []
  #[dD2_dt]
  #  type = TimeDerivative
  #  variable = D2
  #[]
  [dD2p_dt]
    type = TimeDerivative
    variable = D2p
  []
[]

[AuxKernels]
  #Density unit conversions
  [Dp_density_aux]
    type = DensityMoles
    variable = Dp_density
    density_log = Dp
    execute_on = 'LINEAR TIMESTEP_END'
  []
  [em_density_aux]
    type = DensityMoles
    variable = em_density
    density_log = em
    execute_on = 'LINEAR TIMESTEP_END'
  []
  [D_density_aux]
    type = DensityMoles
    variable = D_density
    density_log = D
    execute_on = 'LINEAR TIMESTEP_END'
  []
  #[D2_density_aux]
  #  type = DensityMoles
  #  variable = D2_density
  #  density_log = D2
  #  execute_on = 'LINEAR TIMESTEP_END'
  #[]
  [D2p_density_aux]
    type = DensityMoles
    variable = D2p_density
    density_log = D2p
    execute_on = 'LINEAR TIMESTEP_END'
  []

  #Molecular neutral density for background gas case
  [D2_density_aux]
    type = ConstantAux
    variable = D2_density
    value = 1e+6
  []

  #Background gas
  [D2_val]
    type = ConstantAux
    variable = D2

    #value = 1e+18
    #value = -13.308344895

    #value = 1e+16
    #value = -17.913515081

    #value = 1e+14
    #value = -22.518685267

    #value = 1e+12
    #value = -27.123855453

    #value = 1e+10
    #value = -31.729025639

    #value = 1e+8
    #value = -36.334195825

    #value = 1e+6
    value = -40.939366011

    execute_on = INITIAL
  []

  #Reaction rate calculation
  [REI1_aux]
    type = ParsedAux
    variable = REI1
    coupled_variables = 'em_density D_density'
    expression = '(1.7628661330328915e+10*em_density*D_density)/6.022e+23'
  []
  [REI2_aux]
    type = ParsedAux
    variable = REI2
    coupled_variables = 'em_density D2_density'
    expression = '(2.7182957212183056e+10*em_density*D2_density)/6.022e+23'
  []
  [REI3_aux]
    type = ParsedAux
    variable = REI3
    coupled_variables = 'em_density D2p_density'
    expression = '(6.230347391224091e+9*em_density*D2p_density)/6.022e+23'
  []
  [RDS1_aux]
    type = ParsedAux
    variable = RDS1
    coupled_variables = 'em_density D2_density'
    expression = '(3.8085391841803265e+9*em_density*D2_density)/6.022e+23'
  []
  [RDS2_aux]
    type = ParsedAux
    variable = RDS2
    coupled_variables = 'em_density D2_density'
    expression = '(1.4387980308002887e+9*em_density*D2_density)/6.022e+23'
  []
  [RDS3_aux]
    type = ParsedAux
    variable = RDS3
    coupled_variables = 'em_density D2p_density'
    expression = '(6.643235489590501e+10*em_density*D2p_density)/6.022e+23'
  []
  [RDS4_aux]
    type = ParsedAux
    variable = REI3
    coupled_variables = 'em_density D2p_density'
    expression = '(6.952473833561004e+8*em_density*D2p_density)/6.022e+23'
  []
  [RRC_aux]
    type = ParsedAux
    variable = RRC
    coupled_variables = 'em_density Dp_density'
    expression = '(5.754799703061313e+2*em_density*Dp_density)/6.022e+23'
  []
[]

[Materials]
  [GasBasics]
    type = GasElectronMoments
    interp_elastic_coeff = false
    interp_trans_coeffs = false
    property_tables_file = ../rate_coefficients/electron_moments.txt
    ramp_trans_coeffs = false
    user_p_gas = 10000
    #em = em
    #mean_en = mean_en
    #user_electron_mobility = ?
    #user_electron_diffusion_coeff = ?
  []
  [gas_species_0]
    type = ADHeavySpecies
    heavy_species_name = Dp
    heavy_species_mass = 3.34e-27
    heavy_species_charge = 1.0
  []
  [gas_species_1]
    type = ADHeavySpecies
    heavy_species_name = D
    heavy_species_mass = 3.34e-27
    heavy_species_charge = 0.0
  []
  [gas_species_2]
    type = ADHeavySpecies
    heavy_species_name = D2p
    heavy_species_mass = 6.68e-27
    heavy_species_charge = 0.0
  []
  [gas_species_3]
    type = ADHeavySpecies
    heavy_species_name = D2
    heavy_species_mass = 6.68e-27
    heavy_species_charge = 0.0
  []
[]

#CRANE's Reactions Action that inputs the reactions as source terms for the variables
[Reactions]
  [Gas]
    #species = 'Dp em D D2 D2p'
    species = 'Dp em D D2p'
    aux_species = 'D2'
    gas_species = 'D2'
    reaction_coefficient_format = 'rate'
    use_log = true
    use_ad = true
    block = 0
    #Define reactions and coefficients
    reactions = 'em + D -> em + em + Dp         : 1.7628661330328915e+10
                 em + D2 -> em + em + D2p       : 2.7182957212183056e+10
                 em + D2p -> em + em + Dp + Dp  : 6.230347391224091e+9
                 em + D2 -> em + D + D          : 3.8085391841803265e+9
                 em + D2 -> em + em + D + Dp    : 1.4387980308002887e+9
                 em + D2p -> em + D + Dp        : 6.643235489590501e+10
                 em + D2p -> D + D              : 6.952473833561004e+8
                 Dp + em -> D                   : 5.754799703061313e+2'
  []
[]

#Initial conditions for variables.
#If left undefine, the IC is zero
[ICs]
  [Dp_ic]
    type = FunctionIC
    variable = Dp
    function = 'log(1e14/6.022e23)'
  []
  [em_ic]
    type = FunctionIC
    variable = em
    function = 'log((1e14 + 1e10)/6.022e23)'
  []
  [D_ic]
    type = FunctionIC
    variable = D
    function = 'log(1e16/6.022e23)'
  []
  #[D2_ic]
  #  type = FunctionIC
  #  variable = D2
  #  function = 'log(1e16/6.022e23)'
  #[]
  [D2p_ic]
    type = FunctionIC
    variable = D2p
    function = 'log(1e10/6.022e23)'
  []
[]

[Functions]
  [density_ic_func]
    type = ParsedFunction
    expression = 'log(1e20/6.022e23)'
  []
[]

#Preconditioning options
#Learn more at: https://mooseframework.inl.gov/syntax/Preconditioning/index.html
[Preconditioning]
  active = 'smp'
  [smp]
    type = SMP
    full = true
  []

  [fdp]
    type = FDP
    full = true
  []
[]

#How to execute the problem.
#Defines type of solve (such as steady or transient),
# solve type (Newton, PJFNK, etc.) and tolerances
[Executioner]
  type = Transient
  end_time = 1e+9
  dt = 1e+5
  dtmin = 1e-20
  #dtmax = 1e-2
  scheme = bdf2
  #scheme = explicit-euler
  solve_type = NEWTON
  #steady_state_detection = true

  petsc_options = '-snes_converged_reason -snes_linesearch_monitor'
  petsc_options_iname = '-pc_type -pc_factor_shift_type -pc_factor_shift_amount -snes_linesearch_minlambda'
  petsc_options_value = 'lu NONZERO 1.e-10 1e-3'

  nl_rel_tol = 1e-08
  l_max_its = 50
[]

#Defines the output type of the file (multiple output files can be define per run)
[Outputs]
  perf_graph = true
  [out]
    type = Exodus
  []
[]
