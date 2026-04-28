def calcular_indice(data):
    total = 0

    total += data.get("edad", 0)
    total += data.get("ninos", 0)
    total += data.get("adultos", 0)

    trabajo = data.get("trabajo", {})
    salud = data.get("salud", {})

    total += trabajo.get("frecuencia", 0)
    total += trabajo.get("coche", 0)
    total += trabajo.get("bici", 0)
    total += trabajo.get("andando", 0)

    total += salud.get("frecuencia", 0)
    total += salud.get("coche", 0)
    total += salud.get("bici", 0)
    total += salud.get("andando", 0)

    return total