'''contains helper function to remove invalid characters that cannot be displayed on led screen'''



def validate_string(input_string):
    '''function is used to remove invalid characters that cannot be displayed on led screen'''
    validated_string = ''.join(filter(validate_function, input_string))
    return validated_string



def validate_function(char):
    '''validate function for use with filter'''
    valid_chars = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 #@&!?{}<>[]();:.,'%*=+-=$_\\/ :-)"

    if valid_chars.find(char) == -1:
        return False
    else:
        return True
