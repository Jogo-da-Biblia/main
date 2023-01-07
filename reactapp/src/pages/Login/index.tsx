import { useContext } from "react";
import { Navigate, useNavigate } from "react-router-dom"
import { Formik, Form } from "formik"
import { ClientContext, useMutation } from 'graphql-hooks'

import { LOGIN_MUTATION } from "./graphql_operations"
import { Container, InputsContainer, SubmitBtn } from "./styles"
import LoginSchema from "./schema"
import { AuthUser } from "./types";

import { useUserData } from "hooks/UseUserData"
import Logo from "assets/jogodabiblia.png"
import InputField from "components/InputField"
import ParagraphError from "components/ParagraphError"


function Login() {
    const [loginUserMutation] = useMutation(LOGIN_MUTATION)
    const { authenticated, setUser, fetchUser } = useUserData()
    const client = useContext(ClientContext)
    const navigate = useNavigate()

    const from = "/perguntas"

    const onSubmit = async (authData: AuthUser) => {
        // const response = await login(data, () => navigate(from, { replace: true }))

        let { username, password } = authData;

        const { data, error } = await loginUserMutation({ variables: { username, password } })

        if (error) {
            console.log(error)
            return error
        }

        const { token } = data.tokenAuth

        localStorage.setItem("jogo_da_biblia-token", token);
        client.setHeader('Authorization', `JWT ${token}`)

        const userData = await fetchUser()
        const { me } = userData.data
        setUser({ ...me, token });
        navigate(from, { replace: true })

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
                        <SubmitBtn type="submit" children="Entrar" />
                    </Form>
                </Container>

            )}
        </Formik>
    )
}

export default Login