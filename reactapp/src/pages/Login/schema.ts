import * as Yup from 'yup';

const LoginSchema = Yup.object().shape({
    username: Yup.string()
    .required("Campo obrigatório"),
    password: Yup.string()
    .min(8, "Senha muito curto!")
    .required("Campo obrigatório")
})

export default LoginSchema;