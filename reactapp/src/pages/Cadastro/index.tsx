import { useState } from "react"
import { Formik, Form } from "formik"
import { ClientContext, useMutation } from 'graphql-hooks'

import CadastroSchema from "./schema"
import { inputData } from "./data"
import { Container, InputsContainer, SubmitBtn } from "./styles"
import { CADASTRO_MUTATION } from "./graphql_operations"

import { IUser } from "global/types/user"
import Logo from "assets/jogodabiblia.png"
import { Checkmark, Label } from "global/styles/globalStyles"
import InputField from "components/InputField"
import ParagraphError from "components/ParagraphError"


interface ICadastroUser extends IUser {
    password_2: string
}

function validatePassword_2(value: string, mainValue: string) {
    if (!value) {
        return "Campo obrigatório";
    } else if (value !== mainValue) {
        return "Campos de senha não conferem";
    }
    return false;
}

function Cadastro() {
    const [cadastrar] = useMutation(CADASTRO_MUTATION)
    const [useTermsChecked, setChecked] = useState(false);

    const onSubmit = async (authData: ICadastroUser) => {

        if (!useTermsChecked) {
            alert("Favor peencher caixa de termos de uso!")
            return;
        }

        const { username, email, whatsappNumber, password } = authData

        const { error } = await cadastrar({
            variables: {
                username,
                email,
                phone: whatsappNumber,
                password
            }
        })

        if (error) {
            return alert(error.graphQLErrors[0].message)
        }

        alert("Conta criada!")
    }

    return (
        <Formik
            initialValues={{
                username: "",
                email: "",
                password: "",
                password_2: "",
                whatsappNumber: ""
            }}
            validationSchema={CadastroSchema}
            onSubmit={onSubmit}
        >
            {({ values, errors, touched }) => (
                <Container>
                    <img className="logo" src={Logo} alt="logo" />
                    <Form>

                        <h1>Cadastrar</h1>
                        <p>Para começar a colaborar cadastre-se com seus dados abaixo e comece a enviar perguntas.</p>

                        <InputsContainer >
                            {inputData.map((d, i) => (
                                <div key={i}>
                                    <InputField
                                        label={d.label}
                                        bordercolor={
                                            errors[d.name as keyof typeof errors]
                                            && touched[d.name as keyof typeof touched]}
                                        type={d.type || "text"}
                                        name={d.name}
                                        value={values[d.name as keyof typeof values]}
                                        validate={
                                            d.name === "password_2" ?
                                                () => validatePassword_2(values.password_2, values.password) : undefined
                                        }
                                    />
                                    {
                                        errors[d.name as keyof typeof errors]
                                        && touched[d.name as keyof typeof touched] && (
                                            <ParagraphError children={errors[d.name as keyof typeof errors]} />
                                        )
                                    }
                                </div>
                            ))}
                        </InputsContainer>
                        <Label className="checkbox-container">
                            Li e concordo com os <a href="/termos-de-uso" target="_blank" >termos de uso</a>
                            <input type="checkbox" onChange={e => setChecked(e.target.checked)} />
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