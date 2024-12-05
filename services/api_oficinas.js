const URL = 'http://127.0.0.1:8000'

export const getOficinas = async() => {
    try {
        const response = await fetch(`${URL}/oficinas`, {
            method: 'GET'
        });
        const data = await response.json();
        console.log(data);
        return data;
    } catch(e) {
        console.error('Error en la solicitud', e)
        throw e;
    }
}

export const addOficinas = async(
    id_propietario,
    nombre,
    ubicacion,
    descripcion,
    capacidad_maxima,
    precio,
    disponibilidad) => {
    try {
        const response = await fetch(`${URL}/oficina`, {
            method: 'POST',
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({id_propietario,
                nombre,
                ubicacion,
                descripcion,
                capacidad_maxima,
                precio,
                disponibilidad}) 
        });
        const data = await response.json();
        console.log(data);
        return data;
    } catch(e) {
        console.error('Error en la solicitud', e)
        throw e;
    }
}
    

 