import React, { ComponentType, useState } from 'react';
import styled from 'styled-components';
import { XCircle, Save } from 'react-feather';
import { EvaluatedKitty } from '../types/EvaluatedKitty';
import ContentEditable from 'react-contenteditable';

interface Props {
    kitty: EvaluatedKitty;
    onDelete?: (name: string) => unknown;
    onRename?: (oldName: string, newName: string) => unknown;
    nameValidator?: (name: string) => boolean;
}

const CardContainer = styled.div`
    display: flex;
    position: relative;
    flex-direction: column;
    align-items: center;
    max-width: 250px;
    max-height: 350px;
    border: 1px solid black;
    box-sizing: border-box;
    padding: 5px 25px 20px 25px;
`;

const Name = styled.span`
    font-size: 20pt;
    flex: none;
`;

const ImageContainer = styled.div`
    flex: 1;
    max-height: 250px;
    overflow: hidden;
`;

const Image = styled.img`
    height: auto;
    width: auto;
    max-width: 100%;
    max-height: 100%;
`;

const CloseIcon = styled(XCircle)`
    position: absolute;
    right: 5px;
    top: 5px;
    color: red;
`;

const SaveIcon = styled(Save)`
    position: absolute;
    right: 30px;
    top: 5px;
`;

export const KittyCard: ComponentType<Props> = ({
    kitty: { name, pictureUrl },
    onDelete,
    onRename,
    nameValidator,
}) => {
    const [originalName, ,] = useState(name);
    const [inputName, setInputName] = useState(name);

    const isPendingNameChange = originalName !== inputName;
    const nameIsValid = nameValidator?.(inputName) ?? true;

    const saveIconColor = !isPendingNameChange
        ? 'gray'
        : !nameIsValid
        ? 'red'
        : 'green';

    return (
        <CardContainer>
            <Name>
                <ContentEditable
                    html={inputName}
                    onChange={(evt) => {
                        setInputName(evt.target.value);
                    }}
                />
            </Name>
            <SaveIcon
                onClick={() =>
                    isPendingNameChange &&
                    nameIsValid &&
                    onRename?.(originalName, inputName)
                }
                color={saveIconColor}
            />
            {onDelete ? <CloseIcon onClick={() => onDelete(name)} /> : null}
            <ImageContainer>
                <Image src={pictureUrl} />
            </ImageContainer>
        </CardContainer>
    );
};
