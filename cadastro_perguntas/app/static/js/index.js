$(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    })
});

$(function () {
    $('.inlineform').formset({
        prefix: '{{ formset.prefix }}',
        addText: 'Adicionar nova alternativa',
        deleteText: 'Remover',
    });
})

$("#versao").change(function () {
    data = $.post(
        "/pergunta/get_capitulos",
        {'livro': $("#livros :selected").val(),
        'versao': $("#versao :selected").val()},
    );

    data.done(function (data) {
        $("#capitulos").children().remove();
        data.forEach(function (item) {
            $("#capitulos").append(
                $("<option></option>").attr("value", item.id).text(item.capitulo, item.versao_id)
            );
        });
    });
});

$("#capitulos").change(function () {
    data = $.post(
        "/pergunta/get_versiculos",
        {'livro': $("#livros :selected").val(),
        'versao': $("#versao :selected").val(),
        'capitulo': $("#capitulos :selected").text(),
        },
    );

    data.done(function (data) {
        $("#versiculos").children().remove();
        data.forEach(function (item) {
            $("#versiculos").append(
                $("<option></option>").attr("value", item.id).text(item.versiculo)
            );
        });
    });
});

$("#versiculos").change(function () {
    data = $.post(
        "/pergunta/get_texto_biblico",
        {'livro': $("#livros :selected").val(),
        'versao': $("#versao :selected").val(),
        'capitulo': $("#capitulos :selected").text(),
        'versiculo': $("#versiculos :selected").text(),
        },
    );

    data.done(function (data) {
        var data_texto = JSON.stringify(data);
        $("#texto_biblico").text(data_texto);
    });
});

$("#btn_salvar").click(function () {
    if ($("#radio_biblia").is(":checked")) {
        esvaziaEscolhaTextual();
    }
    if ($("#radio_textual").is(":checked")) {
        esvaziaEscolhaBiblica();
    }
});

$("#radio_biblia").change(function () {
    if ($(this).is(":checked")) {
        $("#section_referencia").show();
        $("#section_textual").hide();
        $("#section_textual").hide();
    }
});

verificaCamposOutrasReferencias()
function verificaCamposOutrasReferencias() {
    if ($("#id_outras_referencias").val() == "") {
        $("#section_textual").hide();
    } else {
        $("#section_textual").show();
    }
}

$("#radio_textual").change(function () {
    if ($(this).is(":checked")) {
        $("#section_textual").show();
        $("#section_referencia").hide();
    }
});

$("#radio-escolha").change(function () {
    if ($(this).is(":checked")) {
        $("#section_alternativa").show();
        $("#section_selecao_referencia").show()
        $("#section_referencia").show();
        verificaCamposOutrasReferencias()
    }
});

$("#radio-completa").change(function () {
    if ($(this).is(":checked")) {
        $("#section_alternativa").hide();
        $("#section_selecao_referencia").hide();        
        $("#section_referencia").show();
        $("#section_textual").hide();
    }
});

$("#radio-livro-capitulo").change(function () {
    if ($(this).is(":checked")) {
        $("#section_alternativa").hide();
        $("#section_selecao_referencia").show();        
        $("#section_referencia").show();
        $("#section_textual").hide();
    }
});

$("#radio-simples").change(function () {
    if ($(this).is(":checked")) {
        $("#section_alternativa").hide();
        $("#section_selecao_referencia").hide();        
        $("#section_referencia").hide();
        $("#section_textual").show();
    }
});

// Garante que campos não selecionados não estejam na requisição POST
function esvaziaEscolhaBiblica() {
    $("#livros").text("");
    $("#versao").text("");
    $("#capitulos").text("");
    $("#versiculos").text("");
    $("#texto_biblico").text("");
}

// Garante que campos não selecionados não estejam na requisição POST
function esvaziaEscolhaTextual() {
    $("#id_texto_biblico").val("");
    $("#id_outras_referencias").val("");
}
