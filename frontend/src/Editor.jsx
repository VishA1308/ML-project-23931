import { LexicalComposer } from '@lexical/react/LexicalComposer';
import { ContentEditable } from '@lexical/react/LexicalContentEditable';
import { HistoryPlugin } from '@lexical/react/LexicalHistoryPlugin';
import { RichTextPlugin } from '@lexical/react/LexicalRichTextPlugin';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { $getRoot, $createParagraphNode, $createTextNode } from 'lexical';
import React, { useEffect, useState } from 'react';

const theme = {
    root: 'p-4 border rounded-md bg-white focus-within:border-blue-500',
    editable: 'outline-none min-h-[200px]',
};

// Create a separate component for editable control
function EditablePlugin({ editable }) {
    const [editor] = useLexicalComposerContext();

    useEffect(() => {
        editor.setEditable(editable);
    }, [editable, editor]);

    return null;
}

function Toolbar() {
    const [editor] = useLexicalComposerContext();

    return (
        <div className="toolbar flex gap-2 mb-2">
            <button
                className="px-2 py-1 bg-gray-100 rounded hover:bg-gray-200"
                onClick={() => editor.update(() => {
                    const root = $getRoot();
                    root.clear();
                    root.append($createParagraphNode());
                })}
            >
                Очистить
            </button>
        </div>
    );
}

function OnChangePlugin({ initialValue, onChange }) {
    const [editor] = useLexicalComposerContext();

    useEffect(() => {
        // Set initial value
        editor.update(() => {
            const root = $getRoot();
            root.clear();
            const paragraph = $createParagraphNode();
            paragraph.append($createTextNode(initialValue));
            root.append(paragraph);
        });

        return editor.registerUpdateListener(({ editorState }) => {
            editorState.read(() => {
                const text = $getRoot().getTextContent();
                onChange(text);
            });
        });
    }, [editor, initialValue, onChange]);

    return null;
}

export function Editor({ initialValue, editable = true, onChange }) {
    const initialConfig = {
        namespace: 'EditableEditor',
        theme,
        editable,
        nodes: [],
        onError: (error) => console.error(error),
        editorState: () => {
            const root = $getRoot();
            if (root.isEmpty()) {
                const paragraph = $createParagraphNode();
                paragraph.append($createTextNode(initialValue));
                root.append(paragraph);
            }
        }
    };

    return (
        <LexicalComposer initialConfig={initialConfig}>
            <div className="editor-wrapper">
                <RichTextPlugin
                    contentEditable={<ContentEditable className={theme.editable} />}
                    placeholder={null}
                />
                <HistoryPlugin />
                <EditablePlugin editable={editable} />
                <Toolbar />
            </div>
            <OnChangePlugin
                initialValue={initialValue}
                onChange={onChange}
            />
        </LexicalComposer>
    );
}