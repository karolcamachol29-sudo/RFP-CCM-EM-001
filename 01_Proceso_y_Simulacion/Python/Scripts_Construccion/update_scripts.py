with open('create_simulacion_pruebas.py', 'r') as f:
    content = f.read()

# Make sure S-05 and S-ZLD_PUR are also set to GlobalDef
content = content.replace("srec_hot_so.find('ForcePhase').text = 'GlobalDef'", """srec_hot_so.find('ForcePhase').text = 'GlobalDef'
    # Ensure S-05 and S-ZLD_PUR are also natural GlobalDef
    if 'S-05' in tag_to_so:
        fp = tag_to_so['S-05'].find('ForcePhase')
        if fp is not None: fp.text = 'GlobalDef'
    if 'S-ZLD_PUR' in tag_to_so:
        fp = tag_to_so['S-ZLD_PUR'].find('ForcePhase')
        if fp is not None: fp.text = 'GlobalDef'""")

with open('create_simulacion_pruebas.py', 'w') as f:
    f.write(content)

with open('verify_simulacion_pruebas.py', 'r') as f:
    vcontent = f.read()

vcontent = vcontent.replace("'S-05': 'Vapor',\n        'S-ZLD_PUR': 'Liquid',", "'S-05': 'GlobalDef',\n        'S-ZLD_PUR': 'GlobalDef',")

with open('verify_simulacion_pruebas.py', 'w') as f:
    f.write(vcontent)

print("Updated create and verify scripts.")
