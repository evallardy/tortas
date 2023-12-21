const numberFormat2 = new Intl.NumberFormat('en-MX', { style: 'decimal', 'fraction': '00' });

function reformatear(obj) {
    objeto = "#" + obj;
    valor = $(objeto).val().replaceAll(",", "").replaceAll(",", "");
    $(objeto).val(numberFormat2.format(valor));
}
function valideKey(evt) {
    var code = (evt.which) ? evt.which : evt.keyCode;
    var value = evt.target.value;
    var hasDecimal = (value.indexOf('.') !== -1);
    if ((code >= 48 && code <= 57) || (code == 46 && !hasDecimal)) {
        return true;
    } else {
        return false;
    }
}
function inicia_consulta(cita) {
    inicia_consulta_cita(cita);
    inicia_consulta_expediente(cita);
}
function inicia_consulta_cita(cita) {
    url = '/cita/inicia_consulta/' + cita  + '/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            $('#citas_del_dia').html(response);
            $('.btn-inicio').hide();
        }
    });
}
function inicia_consulta_expediente(cita) {
    url = '/paciente/pacientes_btn/' + cita  + '/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            $('#pacientes').html(response);
            var input = $('<input>', {
                type: 'text',
                name: 'cita',
                id: 'id_cita',
                value: cita,
                hidden: true
              });
            $('#area-expedientes').append(input);
//            $('#registro-de-pacientes').show();
//            $('#id-nombre-paciente').show();
//            $('#success-nuevo').show();
//            $('#btn-success-nuevo').show();
        }
    });
}
function termina_consulta(cita) {
    url = '/cita/termina_consulta/' + cita  + '/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            $('#citas_del_dia').html(response);
            cita_empieza = '#empieza-cita-' + cita;
            hora_inicio_cita_actual = $.trim($(cita_empieza).html());
            $('#empieza-cita-guarda').val(hora_inicio_cita_actual);
            $('#frm-consulta').submit();
        }
    });
}
function inicia_datos_paciente() {
    $('#id-paciente').val('0');
    $('#datos-nvo-cliente').show()
    $('#id-nombre-paciente').val('');
    datos_paciente(0);
}
function selecciona_paciente(id) {
    $('#expediente-citas').show();
    $('#datos-cita').show();
    limpia_datos_cliente_nvo();
    datos_paciente(id);
}
function limpia_datos_cliente_nvo() {
    $('#id-nombre-cliente').val('');
    $('#id-celular').val('');
    $('#id-correo').val('');
    $('#id-fecha-nac').val('');
    $('#id-genero').val('0');
    $('#id-estado-civil').val('0');
    $('#id-ocupacion').val('');
    $('#id-nacionalidad').val('');
}
function datos_citas_paciente(id) {
    $.ajax({
        url: '/expediente/datos_citas_paciente/' + id + "/",
        type: 'GET',
        success: function(response) {

        }
    });
}
function datos_paciente(id) {
    $.ajax({
        url: '/paciente/datos_paciente/' + id + "/",
        type: 'GET',
        success: function(response) {
            $('#expediente-cliente').html(response);
            if (id == '0') {
                $('#id-celular').val($('#id-celular-memoria').val());
            } else {
                datos_citas_paciente(id);
                $('#datos-nvo-cliente').hide()
                if ($('#mensaje-nombre-paciente').length) {
                    $('#mensaje-nombre-paciente').remove();
                }
                if ($('#mensaje-celular-paciente').length) {
                    $('#mensaje-celular-paciente').remove();
                }
                if ($('#mensaje-correo-paciente').length) {
                    $('#mensaje-correo-paciente').remove();
                }
                if ($('#mensaje-fecha-nac-paciente').length) {
                    $('#mensaje-fecha-nac-paciente').remove();
                }
                if ($('#mensaje-genero-paciente').length) {
                    $('#mensaje-genero-paciente').remove();
                }
                if ($('#mensaje-estado-civil-paciente').length) {
                    $('#mensaje-estado-civil-paciente').remove();
                }
                if ($('#mensaje-expediente').length) {
                    $('#mensaje-expediente').remove();
                }
            }
        }
    });
}
function confirmacion(titulo, contenido, url_ok, url_nok, texto_ok, texto_nok) {
    $.confirm({
        theme: 'Material',
        title: titulo,
        icon: 'fa fa-info',
        content: contenido,
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: 'Si',
                btnClass: 'btn-green',
                action: function(){
                    document.location.href = url_ok;
                    $.alert(texto_ok);
                }
            },
            info1: {
                text: 'No',
                btnClass: 'btn-red',
                keys:['esc'],
                action: function(){
                    if (url_nok != "") {
                        document.location.href = url_nok;
                    }
                    $.alert(texto_nok);
                }
            },
        }
    });
}
function armadoFecha(fecha){
    var mes = fecha.getMonth() + 1;
    var fechaConvertida = fecha.getFullYear() + '-' + 
        mes.toString().padStart(2, '0') + '-' +
        fecha.getDate().toString().padStart(2, '0') + ' ' +
        fecha.getHours().toString().padStart(2, '0') + ':' +
        fecha.getMinutes().toString().padStart(2, '0') + ':' +
        fecha.getSeconds().toString().padStart(2, '0');
        return fechaConvertida;
}
function aviso(titulo, contenido) {
    $.confirm({
//        theme: 'Material',
        title: titulo,
        icon: 'fa fa-info',
        content: contenido,
//        columnClass: 'small',
        autoClose: false,
//        typeAnimated: true,
//        cancelButtonClass: 'btn-primary',
//        draggable: true,
//        dragWindowBorder: false,
        buttons: {
            buttonName: {
                text: 'OK',
                btnClass: 'btn-blue',
//                keys:['esc','enter'],
            }
        }
    });
}
function cuadro(objeto_id, objeto_lb) {
    objeto_lb.removeClass("form-check-label");
    objeto_lb.after(objeto_id);
    objeto_id.removeClass("checkboxinput");
    objeto_id.removeClass("form-check-input");
    objeto_id.css("display", "block");
    objeto_id.css("text-align", "center");
    objeto_id.css("width", objeto_lb.css("width"));
//    objeto_id.css("margin-top", "5px");
    objeto_id.css("height", "25px");
}

// const numberFormat2 = new Intl.NumberFormat('en-MX',{ style:'decimal', 'fraction':'00' });

//function reformatear(obj) {
//    objeto = "#"+obj;
//    valor= $(objeto).val().replaceAll(",", "").replaceAll(",", "");
//    $(objeto).val(numberFormat2.format(valor));
//}
function valideKey(evt){
    var code = (evt.which) ? evt.which : evt.keyCode;
    if (code == 46) {
      return true;
    } else {
        if(code>=48 && code<=57) {
            return true;
        } else{
            return false;
        }
    }
}
function valideKeySinPunto(evt){
    var code = (evt.which) ? evt.which : evt.keyCode;
    if(code>=48 && code<=57) {
        return true;
    } else{
        return false;
    }
}
function convierteNumero(campo,opcion) {
    deCampo = "#" + campo;
    if (opcion == 0) {
        a = parseFloat($(deCampo).val().replace(",","").replace(",",""));
    } else {
        a = parseFloat($(deCampo).val().replace(",","").replace(",","")).toFixed(2);
    }
    resultado = 0;
    if ((isNaN(a)) ||  (a == null)) {
        resultado = 0;
    } else {
        resultado = a;
    }
    return resultado;
}
function verDato(campo) {
    deCampo = "#id_" + campo;
    alert(campo + " : " + $(deCampo).val());
}
function validaNumero(campo) {
    if (isNaN(campo) || campo=="" || campo==0) {
        return false;
    }
    return true;
}
function validaCadena(campo) {
    if (isNaN(campo) || campo.trim()=="") {
        return false;
    }
    return true;
}
function soloNumeros(evt){
    var code = (evt.which) ? evt.which : evt.keyCode;
    if(code>=48 && code<=57) {
        return true;
    } else{
        return false;
    }
}
function soloNumerosConPunto(evt){
    var code = (evt.which) ? evt.which : evt.keyCode;
    if (code == 46) {
      return true;
    } else {
        if(code>=48 && code<=57) {
            return true;
        } else{
            return false;
        }
    }
}
