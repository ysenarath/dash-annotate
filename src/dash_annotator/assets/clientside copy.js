// assets/clientside.js
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        handleTextSelection: function (textarea_props) {
            let currentID = textarea_props.id;

            // Find the textarea using a more reliable selector
            // that avoids issues with browser autofill services
            const textareas = document.getElementsByTagName('textarea');
            let textarea = null;

            // Find the textarea with matching data attributes
            for (let t of textareas) {
                const checkID = JSON.parse(t.id).id;
                if (checkID === currentID) {
                    textarea = t;
                    break;
                }
            }

            if (!textarea) return null;

            // Disable autofill on the textarea
            textarea.setAttribute('autocomplete', 'off');
            textarea.setAttribute('data-form-type', 'other');
            textarea.setAttribute('data-lpignore', 'true');

            // function updateSelection() {
            //     const start = textarea.selectionStart;
            //     const end = textarea.selectionEnd;
            //     console.log("Selection Start: " + start);
            //     console.log("Selection End: " + end);
            //     if (start !== end) {
            //         return {
            //             start: start,
            //             end: end
            //         };
            //     }
            //     return null;
            // }

            // // Add event listeners for selection changes
            // textarea.addEventListener('select', updateSelection);
            // textarea.addEventListener('mouseup', updateSelection);
            // textarea.addEventListener('keyup', updateSelection);

            // // Return initial selection state
            // return updateSelection();
        }
    }
});
