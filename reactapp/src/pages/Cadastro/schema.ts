import * as Yup from 'yup';

const CadastroSchema = Yup.object().shape({
    username: Yup.string()
    .min(3, "muito curto")
    .max(50, "muito longo")
    .required("Campo obrigatório"),
    email: Yup.string()
    .email("Formato inválido")
    .required("Campo obrigatório"),
    password: Yup.string()
    .min(8, "Senha muito curto!")
    .required("Campo obrigatório"),
    whatsappNumber: Yup.string()
    .min(8, "Muito curto!")
    .max(14, "Muito longo!")
    .required("Campo obrigatório")
})

export default CadastroSchema;