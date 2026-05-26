import { createResource } from 'frappe-ui'

export default function translationPlugin(app) {
	app.config.globalProperties.__ = translate
	window.__ = translate
	if (!window.translatedMessages) {
		const guestLang = localStorage.getItem('lms_lang') || undefined
		fetchTranslations(guestLang)
	}
}

function translate(message) {
	let translatedMessages = window.translatedMessages || {}
	let translatedMessage = translatedMessages[message] || message

	const hasPlaceholders = /{\d+}/.test(message)
	if (!hasPlaceholders) {
		return translatedMessage
	}
	return {
		format: function (...args) {
			return translatedMessage.replace(
				/{(\d+)}/g,
				function (match, number) {
					return typeof args[number] != 'undefined'
						? args[number]
						: match
				}
			)
		},
	}
}

function fetchTranslations(lang) {
	createResource({
		url: 'lms.lms.api.get_translations',
		params: lang ? { lang } : {},
		cache: ['translations', lang || 'default'],
		auto: true,
		transform: (data) => {
			window.translatedMessages = data
		},
	})
}
