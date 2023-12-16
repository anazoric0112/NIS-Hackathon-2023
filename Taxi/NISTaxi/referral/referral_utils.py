import base64

def generate_referral_code(taxilicence : str):
    taxilicence_bytes = taxilicence.encode('utf-8')

    referral_code = base64.urlsafe_b64encode(taxilicence_bytes).decode('utf-8')

    return referral_code

def decode_referral_code(ref_code_b64 : str):
    ref_code = base64.b64decode(ref_code_b64)
    ref_code = ref_code.decode('utf-8')

    return ref_code

print(generate_referral_code('11229'))