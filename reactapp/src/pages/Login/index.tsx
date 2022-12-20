import { Navigate, useNavigate } from "react-router-dom"
import { useUserData } from "hooks/UseUserData"
import { Formik, Form } from "formik"
import LoginSchema from "./schema"
import { AuthUser } from "types/user"
import { Container, InputsContainer, StyledField, SubmitBtn } from "./styles"
import Logo from "assets/jogodabiblia.png"

function Login() {
    const { authenticated, login } = useUserData()
    const navigate = useNavigate()

    const from = "/perguntas"

    const onSubmit = async (data: AuthUser) => {
        // if (login) {
        //     login(data, () => navigate(from, { replace: true }))
        // }
        console.log(data)
    }

    if (authenticated) {
        return (
            <Navigate to="perguntas" replace />
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
            {({ errors, touched }) => (
                <Container>
                    <img className="logo" src={Logo} alt="logo" />
                    <Form>
                        <h1>Login</h1>
                        <p>Colabore conosco. Digite abaixo seu usuário e senha para começar a cadastrar suas perguntas.</p>
                        <InputsContainer >
                            <StyledField
                                bordercolor={errors.username && touched.username ? 'red' : ''}
                                placeholder="Username ou Email"
                                type="username"
                                name="username"
                            />
                            <StyledField
                                bordercolor={errors.password && touched.password ? 'red' : ''}
                                placeholder="Senha"
                                type="password"
                                name="password"
                            />
                        </InputsContainer>
                        <SubmitBtn children="Entrar" />
                    </Form>
                </Container>

            )}
        </Formik>
    )
}

export default Login