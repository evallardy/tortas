const files = document.querySelectorAll('.campo-file')
Array.from(files).forEach(
    f => {
        f.addEventListener('change', e => {
            campo = f.id.substring(3,);
            const icono_muestra = $('#muestra_archivo_' + campo);
            const borra_muestra = $('#borra_archivo_' + campo);
//            const imagen = document.querySelector(icono_muestra);
//            const span = document.querySelector(icono_muestra);

            const archivo_temporal = '#id_texto_' + campo;
            const temporal = $(archivo_temporal);

//            const elemento = document.createElement("img");
//            const no_elemento = document.createElement("img");

//            elemento.src = "/static/core/img/comprobante.svg";
//            elemento.width = 25;
//            const elementoLleno = "/static/core/img/comprobante.svg";
//            no_elemento.src = "/static/core/img/vacio.svg";
//            no_elemento.width = 25;
//            const elementoVacio = "/static/core/img/vacio.svg";
//            span.innerHTML = "";

            if (f.files.length == 0) {
                temporal.val("");
//                span.appendChild(no_elemento);
                icono_muestra.attr('src', "/static/core/img/vacio.svg");
                borra_muestra.hide();
//                imagen.src  = elementoVacio;
            } else {
                const archivoSeleccionado = e.target.files[0];
                temporal.val(URL.createObjectURL(archivoSeleccionado));
//                temporal.val(objectURL);
//                span.appendChild(elemento);
                icono_muestra.attr('src', "/static/core/img/comprobante.svg");
                borra_muestra.show();
//                imagen.src  = elementoLleno;
            }
        })
    }
);
