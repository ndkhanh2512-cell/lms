<template>
	<div class="flex items-center text-sm select-none">
		<button
			@click="setLang('en')"
			:class="
				currentLang === 'en'
					? 'font-bold text-ink-gray-9'
					: 'text-ink-gray-5 hover:text-ink-gray-7'
			"
			class="px-1.5 py-1 min-h-[36px]"
			aria-label="English">
			EN
		</button>
		<span class="text-ink-gray-3">|</span>
		<button
			@click="setLang('vi')"
			:class="
				currentLang === 'vi'
					? 'font-bold text-ink-gray-9'
					: 'text-ink-gray-5 hover:text-ink-gray-7'
			"
			class="px-1.5 py-1 min-h-[36px]"
			aria-label="Tiếng Việt">
			VI
		</button>
	</div>
</template>

<script setup>
import { computed } from 'vue'
import { call } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/user'

const { isLoggedIn } = sessionStore()
const { userResource } = usersStore()

const currentLang = computed(() => {
	if (isLoggedIn.value && userResource?.data?.language) {
		return userResource.data.language
	}
	return localStorage.getItem('lms_lang') || 'en'
})

async function setLang(newLang) {
	if (newLang === currentLang.value) return

	localStorage.setItem('lms_lang', newLang)

	if (isLoggedIn.value && userResource?.data?.name) {
		try {
			await call('frappe.client.set_value', {
				doctype: 'User',
				name: userResource.data.name,
				fieldname: 'language',
				value: newLang,
			})
		} catch (e) {
			console.error('Failed to update user language', e)
		}
	}
	window.location.reload()
}
</script>
