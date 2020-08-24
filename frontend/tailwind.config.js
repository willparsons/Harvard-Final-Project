module.exports = {
    future: {
        removeDeprecatedGapUtilities: true,
    },
    theme: {
        extend: {
            fontFamily: {
                roboto: ["Roboto"],
            },
        },
    },
    variants: {},
    plugins: [require("@tailwindcss/custom-forms")],
};
