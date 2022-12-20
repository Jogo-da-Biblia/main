import { IUser } from "types/user"
import { Formik, Form } from "formik"
import CadastroSchema from "./schema"
import Logo from "assets/jogodabiblia.png"
import { Container, InputsContainer, StyledField, SubmitBtn } from "./styles"
import { Checkmark, Label } from "styles/globalStyles"
import { useState } from "react"

interface ICadastroUser extends IUser {
    password_2: string
}

// function validatePassword_2(value, mainValue) {
//     if (!value) {
//         return "PREENCHIMENTO OBRIGATÓRIO";
//     } else if (value !== mainValue) {
//         return "CAMPOS DE SENHA NÃO CONFEREM";
//     }
//     return false;
// }

function Cadastro() {
    const [useTermsChecked, setChecked] = useState(false);

    const onSubmit = async (data: ICadastroUser) => {
        console.log(data)
    }

    return (
        <Formik
            initialValues={{
                username: "",
                email: "",
                password: "",
                password_2: "",
                whatsappNumber: null
            }}
            validationSchema={CadastroSchema}
            onSubmit={onSubmit}
        >
            {({ errors, touched }) => (
                <Container>
                    <img className="logo" src={Logo} alt="logo" />
                    <Form>

                        <h1>Login</h1>
                        <p>Para começar a colaborar cadastre-se com seus dados abaixo e comece a enviar perguntas.</p>
                        <InputsContainer >
                            <StyledField
                                bordercolor={errors.username && touched.username ? 'red' : ''}
                                placeholder="Username"
                                type="text"
                                name="username"
                            />
                            <StyledField
                                bordercolor={errors.email && touched.email ? 'red' : ''}
                                placeholder="Email"
                                type="email"
                                name="email"
                            />
                            <StyledField
                                bordercolor={errors.password && touched.password ? 'red' : ''}
                                placeholder="Digite sua senha"
                                type="password"
                                name="password"
                            />
                            <StyledField
                                bordercolor={errors.password_2 && touched.password_2 ? 'red' : ''}
                                placeholder="Confirme sua senha"
                                type="password"
                                name="password_2"
                            />
                            <StyledField
                                bordercolor={errors.whatsappNumber && touched.whatsappNumber ? 'red' : ''}
                                placeholder="Whatsapp"
                                type="phone"
                                name="whatsappNumber"
                            />
                        </InputsContainer>
                        <Label className="checkbox-container">
                            Li e concordo com os <a href="/termos-de-uso" target="_blank" >termos de uso</a>
                            <input type="checkbox" onClick={e => setChecked(true)} />
                            <Checkmark />
                        </Label>
                        <SubmitBtn children="Cadastrar" />
                    </Form>
                </Container>

            )}
        </Formik>
    )
}

export default Cadastro