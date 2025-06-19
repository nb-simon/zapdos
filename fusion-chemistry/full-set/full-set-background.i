#Testing implementation of simple fusion reactions at the pedestal
#Assumptions:
# temperature = 0.5 keV
# deuterium density = 3e20 m^-3

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
  [D+]
  []
  #[T+]
  #[]
  #[He+]
  #[]
  [em]
  []
  [D]
  []
  [D2+]
  []
  #[potential]
  #[]
  #[mean_en]
  #[]
[]

[AuxVariables]
  [D+_density]
    order = CONSTANT
    family = MONOMIAL
  []
  #[T+_density]
  #  order = CONSTANT
  #  family = MONOMIAL
  #[]
  #[He+_density]
  #  order = CONSTANT
  #  family = MONOMIAL
  #[]
  [em_density]
    order = CONSTANT
    family = MONOMIAL
  []
  [D_density]
    order = CONSTANT
    family = MONOMIAL
  []
  [D2+_density]
    order = CONSTANT
    family = MONOMIAL
  []

  #Background gas
  [D2]
  []
[]

[Kernels]
  #Adds the time derivative for the variables
  [D+_time_derv]
    type = TimeDerivative
    variable = D+
  []
  #[T+_time_derv]
  #  type = TimeDerivative
  #  variable = T+
  #[]
  #[He+_time_derv]
  #  type = TimeDerivative
  #  variable = He+
  #[]
  [em_time_derv]
    type = TimeDerivative
    variable = em
  []
  [D_time_derv]
    type = TimeDerivative
    variable = D
  []
  [D2+_time_derv]
    type = TimeDerivative
    variable = D2+
  []
[]

[AuxKernels]
  [D+_density_aux]
    type = DensityMoles
    variable = D+_density
    density_log = D+
    execute_on = 'LINEAR TIMESTEP_END'
  []
  #[T+_density_aux]
  #  type = DensityMoles
  #  variable = T+_density
  #  density_log = T+
  #  execute_on = 'LINEAR TIMESTEP_END'
  #[]
  #[He+_density_aux]
  #  type = DensityMoles
  #  variable = He+_density
  #  density_log = He+
  #  execute_on = 'LINEAR TIMESTEP_END'
  #[]
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
  [D2+_density_aux]
    type = DensityMoles
    variable = D2+_density
    density_log = D2+
    execute_on = 'LINEAR TIMESTEP_END'
  []

  #Background gas
  [D2_val]
    type = ConstantAux
    variable = D2

    #value = 1e+18
    #value = -13.308344895

    #value = 1e+16
    value = -17.913515081

    execute_on = INITIAL
  []
[]

#[DriftDiffusionAction]
#  [Plasma]
#    electrons = em
#    charged_particle = ?
#    field = potential
#    Is_field_unique = ?
#    mean_energy = mean_en
#    position_units = ?
#    Additional_Outputs = 'ElectronTemperature Current EField'
#  []
#[]

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
    heavy_species_name = D+
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
    heavy_species_name = D2+
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
    #Name of each variable on the reactant side
    species = 'D+ em D D2+'
    aux_species = 'D2'
    gas_species = 'D2'
    #Define type of coefficient (rate or townsend)
    reaction_coefficient_format = 'rate'
    #Define if using log form
    use_log = true
    #Define if using automatic differentiation
    use_ad = true
    #Define which material block the reactions take place.
    # For undefine blocks, naming starts at 0
    block = 0
    #Define reactions and coefficients
    reactions = 'em + D -> em + em + D+         : 2.5856251254792084e+10
                 em + D2 -> em + em + D2+       : 3.578771689937389e+10
                 em + D2+ -> em + em + D+ + D+  : 1.2086215582464874e+10
                 em + D2 -> em + D + D          : 2.563788698395377e+9
                 em + D2 -> em + em + D + D+    : 2.669678563960102e+9
                 em + D2+ -> em + D + D+        : 6.1629154222942116e+10
                 em + D2+ -> D + D              : 1.3595389098887977e+8
                 D+ + D2 -> D + D2+             : 8.85016857412739e+9
                 D+ + em -> D                   : 5.364987086029923e+2'
  []
[]

#Initial conditions for variables.
#If left undefine, the IC is zero
[ICs]
  [D+_ic]
    type = FunctionIC
    variable = D+
    function = 'log(1e20/6.022e23)'
  []
  [em_ic]
    type = FunctionIC
    variable = em
    function = 'log((1e20 + 1e14)/6.022e23)'
  []
  [D_ic]
    type = FunctionIC
    variable = D
    function = 'log(1e16/6.022e23)'
  []
  [D2+_ic]
    type = FunctionIC
    variable = D2+
    function = 'log(1e14/6.022e23)'
  []
  #[mean_en_ic]
  #  type = FunctionIC
  #  variable = mean_en
  #  function = energy_density_ic_func
  #[]
  #[potential_ic]
  #  type = FunctionIC
  #  variable = potential
  #  function = potential_ic_func
  #[]
[]

[Functions]
  [density_ic_func]
    type = ParsedFunction
    expression = 'log(1.5e20/6.022e23)'
  []
  #[energy_density_ic_func]
  #  type = ParsedFunction
  #  expression = 'log(3./2.) + log(3e20/6.022e23)'
  #[]
  #[potential_ic_func]
  #  type = ParsedFunction
  #  expression = '1'
  #[]
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
  #1e+16 background
  end_time = 5.89982
  dt = 1e-4

  #1e+18 background
  #end_time = 0.0933472
  #dt = 1e-5

  dtmin = 1e-14
  scheme = bdf2
  solve_type = NEWTON
  steady_state_detection = true

  petsc_options = '-snes_converged_reason -snes_linesearch_monitor'
  petsc_options_iname = '-pc_type -pc_factor_shift_type -pc_factor_shift_amount -snes_linesearch_minlambda'
  petsc_options_value = 'lu NONZERO 1.e-10 1e-3'

  nl_rel_tol = 1e-08
  l_max_its = 20
[]

#Defines the output type of the file (multiple output files can be define per run)
[Outputs]
  perf_graph = true
  [out]
    type = Exodus
  []
[]
