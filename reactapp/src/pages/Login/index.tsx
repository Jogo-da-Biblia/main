import { Navigate, useNavigate } from "react-router-dom"
import { useUserData } from "hooks/UseUserData"
import { Formik, Form } from "formik"
import LoginSchema from "./schema"
import { AuthUser } from "types/user"
import { Container, InputsContainer, StyledField, SubmitBtn } from "./styles"
import Logo from "assets/jogodabiblia.png"
import InputField from "components/InputField"
import ParagraphError from "components/ParagraphError"

function Login() {
    const { authenticated, login } = useUserData()
    const navigate = useNavigate()

    const from = "/perguntas"

    const onSubmit = async (data: AuthUser) => {
        // if (login) {
        //     login(data, () => navigate(from, { replace: true }))
        // }
        alert(JSON.stringify(data, null, 2))
    }

    if (authenticated) {
        return (
            <Navigate to={from} replace />
        )
    }

    return (
        <Formik
            initialValues={{
                username: "",
                password: ""
            }}
            validationSchema={LoginSchema}
            onSubmit={onSubmit}
        >
            {({ values, errors, touched }) => (
                <Container>
                    <img className="logo" src={Logo} alt="logo" />
                    <Form>
                        <h1>Login</h1>
                        <p>Colabore conosco. Digite abaixo seu usuário e senha para começar a cadastrar suas perguntas.</p>
                        <InputsContainer >
                            <InputField
                                label="Username ou Email"
                                bordercolor={
                                    errors.username
                                    && touched.username}
                                type="text"
                                name="username"
                                value={values.username}
                            />
                            {
                                errors.username && touched.username && (
                                    <ParagraphError children={errors.username} />
                                )
                            }
                            <InputField
                                label="Senha"
                                bordercolor={
                                    errors.password
                                    && touched.password}
                                type="password"
                                name="password"
                                value={values.password}
                            />
                            {
                                errors.password && touched.password && (
                                    <ParagraphError children={errors.password} />
                                )
                            }
                        </InputsContainer>
                        <SubmitBtn children="Entrar" />
                    </Form>
                </Container>

            )}
        </Formik>
    )
}

export default Login