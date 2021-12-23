import axios from 'axios';
import { Formik } from 'formik';
import { useRouter } from 'next/router';
import { useContext } from 'react';
import styled from 'styled-components';
import { AuthContext } from '../components/context/AuthContext';

const Container = styled.div`
    padding-top: 20vh;
`;

const Form = styled.form`
    display: flex;
    flex-direction: column;
    gap: 10px;
    justify-content: center;
    margin: 0 auto 0 auto;
    width: 300px;
`;

const FormRow = styled.div`
    display: flex;
    justify-content: space-between;
`;

const SubmitButton = styled.button`
    max-width: 100px;
    margin: 0 auto 0 auto;
`;

const Login = () => {
    const { setToken } = useContext(AuthContext);
    const router = useRouter();

    return (
        <Container>
            <Formik
                initialValues={{ username: '', password: '' }}
                onSubmit={async (values, { setSubmitting }) => {
                    await axios
                        .post<{ token: string }>(
                            `http://${process.env.NEXT_PUBLIC_API_URL}/api/register`,
                            values
                        )
                        .then(({ data: { token } }) => {
                            setToken?.(token);
                            router.push('/');
                        })
                        .catch((err) => {
                            if ('response' in err) {
                                const errorMessage = `${err.response.status}: ${err.response.data?.error}`;

                                console.error(errorMessage);
                            }
                        });

                    setSubmitting(false);
                }}
            >
                {({
                    handleChange,
                    isSubmitting,
                    errors,
                    touched,
                    values,
                    handleBlur,
                    handleSubmit,
                }) => (
                    <Form onSubmit={handleSubmit}>
                        <FormRow>
                            <label htmlFor="username">Username:</label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.username}
                            >
                                {errors.username &&
                                    touched.username &&
                                    errors.username}
                            </input>
                        </FormRow>
                        <FormRow>
                            <label htmlFor="password">Password:</label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                value={values.password}
                                onChange={handleChange}
                                onBlur={handleBlur}
                            >
                                {errors.password &&
                                    touched.password &&
                                    errors.password}
                            </input>
                        </FormRow>
                        <SubmitButton type="submit" disabled={isSubmitting}>
                            Log in
                        </SubmitButton>
                    </Form>
                )}
            </Formik>
        </Container>
    );
};

export default Login;
