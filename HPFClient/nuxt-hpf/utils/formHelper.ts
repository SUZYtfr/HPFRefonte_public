import { ToastProgrammatic as Toast } from 'buefy'

export type VForm = Vue & { checkValidity: () => boolean }

export const regexPasswordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_\-^~#\|`\\\/\[\]\(\)\{\}=+*\.;:§<>²°])[A-Za-z\d@$!%*?&_\-^~#\|`\\\/\[\]\(\)\{\}=+*\.;:§<>²°]{8,32}$/;

export const OpenToast = (message: string, type: string, duration: number, indefinite: boolean, pauseOnHover: boolean, position: any) =>
Toast.open({
    duration: duration,
    message: message,
    position: position,
    type: type,
    pauseOnHover: pauseOnHover,
    indefinite: indefinite
})
