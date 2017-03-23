# This file contains the human-decided attributes of the incoming metadata

# variable names should be self-explanatory
has_dollarsign = ['X4', 'X5', 'X6']

has_percentsign =['X1', 'X30']

loan_id='X2'
regressand = 'X1'
applicant_id='X3'

scale_fields=['X4', 'X5', 'X6', 'X13', 'X21', 'X29', 'X30']

nominal_fields = ['X12','X14','X19','X20', 'X32']
#TODO  X8 ordinal?
ordinal_fields = [ 'X7','X8','X10','X11','X22', 'X24','X25','X26','X27','X28', 'X31','X9']
#ordinal_but_scale = ['X22','X27', 'X31', 'X11']
string_fields = ['X10', 'X16', 'X17', 'X18']

date_fields = ['X15', 'X23']

discontinuity_to_high = []
has_phrase_months = 'X7'
has_phrase_years = 'X11'
to_scale_fields = ['X11', 'X22', 'X24', 'X27', 'X28', 'X31']
# We exclude some fields from inclusion, such as generic comments by users, for this more limited purpose.
# However, we do acknowledge there may be information there, such as a word count metric, or a count
# of certain words such as 'bankruptcy' that may be of value in a more thorough analysis.
exclude_fields_from_eqn = string_fields + ['X19','X15','X26']