window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        handleTextSelection: function(id) {
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                const textarea = document.querySelector(`#${id}`);
                if (textarea && range.startContainer.parentElement.id === id) {
                    return {
                        start: textarea.selectionStart,
                        end: textarea.selectionEnd
                    };
                }
            }
            return null;
        }
    }
});
