import axios from 'axios';
import type { NextPage } from 'next';
import { useQuery } from 'react-query';
import PulseLoader from 'react-spinners/PulseLoader';
import { KittyGallery } from '../components/KittyGallery';
import { ProtectedRoute } from '../components/ProtectedRoute';
import { EvaluatedKitty } from '../types/EvaluatedKitty';
import { Kitty } from '../types/Kitty';
import { useContext } from 'react';
import { AuthContext } from '../components/context/AuthContext';
import styled from 'styled-components';

const objectivelyBestName = 'James';

const getAwesomenessOfName = (name: string) =>
    name === objectivelyBestName
        ? Infinity
        : [...name].reduce((sum, char) => sum + (char.codePointAt(0) ?? 0), 0);

const sortKitties = (kitties: EvaluatedKitty[]): EvaluatedKitty[] =>
    [...kitties].sort((a, b) => b.awesomeness - a.awesomeness);

const LoaderContainer = styled.div`
    margin: 0 auto 0 auto;
    width: 200px;
    padding-top: 50px;
`;

const Home: NextPage = () => {
    const { token, isAdmin } = useContext(AuthContext);

    const {
        data: kitties,
        isLoading,
        error,
        refetch,
    } = useQuery<EvaluatedKitty[]>('kitties', async () =>
        axios
            .get(`http://${process.env.NEXT_PUBLIC_API_URL}/api/kitties`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((resp) =>
                sortKitties(
                    (resp.data as Kitty[]).map((kitty) => ({
                        ...kitty,
                        awesomeness: getAwesomenessOfName(kitty.name),
                    }))
                )
            )
    );

    if (isLoading) {
        return (
            <LoaderContainer>
                <PulseLoader />
            </LoaderContainer>
        );
    }

    if (error || !kitties) {
        return <div>{`${error || 'Error in kitty processing'}`}</div>;
    }

    const deleteKitty = async (name: string) => {
        axios
            .delete(
                `http://${process.env.NEXT_PUBLIC_API_URL}/api/kitties/${name}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )
            .then(() => refetch());
    };

    const renameKitty = async (oldName: string, newName: string) =>
        axios
            .put(
                `http://${process.env.NEXT_PUBLIC_API_URL}/api/kitties/${oldName}`,
                { newName },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )
            .then(() => refetch());

    return (
        <KittyGallery
            kitties={kitties}
            onDelete={isAdmin?.() ? deleteKitty : undefined}
            onRename={renameKitty}
        />
    );
};

export default ProtectedRoute(Home);
