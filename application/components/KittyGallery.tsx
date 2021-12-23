import React, { ComponentType } from 'react';
import styled from 'styled-components';
import { EvaluatedKitty } from '../types/EvaluatedKitty';
import { KittyCard } from './KittyCard';

interface Props {
    kitties: EvaluatedKitty[];
    onDelete?: (name: string) => unknown;
    onRename?: (oldName: string, newName: string) => unknown;
}

const Container = styled.div`
    display: flex;
    margin: 0 auto 0 auto;
    width: 100%;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 25px;
`;

const KittyItem = styled.div`
    display: flex;
    width: 500px;
    align-items: center;
    justify-content: space-between;
`;

const KittyScoreContainer = styled.div`
    display: grid;
    grid-template-columns: 50% 50%;
    min-width: 250px;
`;

const KittyScore = ({
    rank,
    awesomeness,
}: {
    rank: number;
    awesomeness: number;
}) => (
    <KittyScoreContainer>
        <span>Rank:</span>
        <span>{rank}</span>
        <span>Awesomeness:</span>
        <span>{awesomeness === Infinity ? '∞' : awesomeness}</span>
    </KittyScoreContainer>
);

export const KittyGallery: ComponentType<Props> = ({
    kitties,
    onDelete,
    onRename,
}) => (
    <Container>
        {kitties?.map((kitty, index) => (
            <KittyItem key={kitty.name}>
                <KittyScore rank={index + 1} awesomeness={kitty.awesomeness} />
                <KittyCard
                    kitty={kitty}
                    onDelete={onDelete}
                    onRename={onRename}
                    nameValidator={(potentialName) =>
                        !kitties.find(({ name }) => name === potentialName)
                    }
                />
            </KittyItem>
        ))}
    </Container>
);
