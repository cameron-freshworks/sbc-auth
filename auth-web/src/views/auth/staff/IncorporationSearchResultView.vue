<template>
      <v-data-table
      class="incorporation-search-results"
      :headers="headersSearchResult"
      :items="searchResult"
      hide-default-footer
      v-if="isVisible"
    >
      <template v-slot:loading>
        Loading...
      </template>
      <template v-slot:[`item.orgType`]="{ item }">
          {{formatType(item)}}
      </template>
      <template v-slot:[`item.account`]="{ item }">
        <span
        :class="{ 'account-color-empty': !isThereAnAffiliatedAccount }"
        >
          {{ item.account }}
        </span>
      </template>
      <template v-slot:[`item.action`]>
        <v-menu
        bottom
        left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
            icon
            v-bind="attrs"
            v-on="on"
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list
          dense
          >
              <v-list-item
              v-for="(action, i) in actions"
              :key="i"
              @click="action.event"
              >
                <v-list-item-icon>
                  <v-icon v-text="action.icon"></v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title v-text="action.title"></v-list-item-title>
                </v-list-item-content>
              </v-list-item>
          </v-list>
        </v-menu>
        <GeneratePasscodeView
        ref="generatePasscodeDialog"
        :businessIdentitifier="currentBusiness.businessIdentifier"
        >
        </GeneratePasscodeView>
      </template>
    </v-data-table>
</template>

<script lang="ts">
import { AccessType, Account } from '@/util/constants'
import { Business, BusinessSearchResultDto } from '@/models/business'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Member, Organization } from '@/models/Organization'
import { AccountSettings } from '@/models/account-settings'
import ConfigHelper from '@/util/config-helper'
import GeneratePasscodeView from '@/views/auth/staff/GeneratePasscodeView.vue'
import { UserSettings } from 'sbc-common-components/src/models/userSettings'
import { namespace } from 'vuex-class'

const OrgModule = namespace('org')
const BusinessModule = namespace('business')

@Component({
  components: {
    GeneratePasscodeView
  }
})
export default class IncorporationSearchResultView extends Vue {
  @OrgModule.State('currentOrganization') private currentOrganization!: Organization
  @OrgModule.Action('addOrgSettings') private addOrgSettings!: (currentOrganization: Organization) => Promise<UserSettings>
  @OrgModule.Action('syncOrganization') private syncOrganization!: (affiliatedOrganizationId: number) => Promise<Organization>
  @OrgModule.Action('syncMembership') private syncMembership!: (affiliatedOrganizationId: number) => Promise<Member>
  @OrgModule.Mutation('setCurrentAccountSettings') private setCurrentAccountSettings!: (accountSettings: AccountSettings) => void
  @BusinessModule.State('currentBusiness') private currentBusiness!: Business

  @Prop({ default: false }) isVisible: boolean
  @Prop() affiliatedOrg: Organization

  $refs: {
    generatePasscodeDialog: GeneratePasscodeView
  }

  private get actions (): object[] {
    if (this.isThereAnAffiliatedAccount) {
      return [
        { title: 'Entity Dashboard',
          icon: 'mdi-view-dashboard',
          event: this.entityDashboardEvent
        },
        { title: 'Manage Account',
          icon: 'mdi-domain',
          event: this.manageAccountEvent
        }
      ]
    } else {
      return [
        { title: 'Entity Dashboard',
          icon: 'mdi-view-dashboard',
          event: this.entityDashboardEvent
        },
        { title: 'Generate Passcode',
          icon: 'mdi-lock-outline',
          event: this.generatePasscodeEvent
        }
      ]
    }
  }

  private get searchResult (): BusinessSearchResultDto[] {
    return [{
      name: this.currentBusiness?.name,
      orgType: this.affiliatedOrg?.orgType,
      account: this.affiliatedOrg?.name || 'No Affiliation',
      businessIdentifier: this.currentBusiness?.businessIdentifier,
      businessNumber: this.currentBusiness?.businessNumber,
      accessType: this.affiliatedOrg?.accessType,
      statusCode: this.affiliatedOrg?.statusCode
    }]
  }
  private readonly headersSearchResult = [
    {
      text: 'Name',
      align: 'left',
      sortable: false,
      value: 'name',
      width: '25%'
    },
    {
      text: 'Entity#',
      align: 'left',
      sortable: false,
      value: 'businessIdentifier',
      width: '25%'
    },
    {
      text: 'Type',
      align: 'left',
      sortable: false,
      value: 'orgType',
      width: '25%'
    },
    {
      text: 'Account',
      sortable: false,
      value: 'account',
      width: '25%'
    },
    {
      text: 'Actions',
      align: 'left',
      sortable: false,
      value: 'action',
      width: '105'
    }
  ]

  private formatType (org:BusinessSearchResultDto): string {
    let orgTypeDisplay = org?.orgType ? org?.orgType === Account.BASIC ? 'Basic' : 'Premium' : 'N/A'
    if (org?.accessType === AccessType.ANONYMOUS) {
      return 'Director Search'
    }
    if (org?.accessType === AccessType.EXTRA_PROVINCIAL) {
      return orgTypeDisplay + ' (out-of-province)'
    }
    return orgTypeDisplay
  }

  private async entityDashboardEvent () {
    window.location.href = `${ConfigHelper.getCoopsURL()}${this.currentBusiness.businessIdentifier}`
  }

  private async manageAccountEvent () {
    try {
      await this.syncOrganization(this.affiliatedOrg.id)
      await this.syncMembership(this.currentOrganization.id)
      await this.addOrgSettings(this.currentOrganization)
      this.$router.push(`/account/${this.currentOrganization.id}/business`)
    } catch (error) {
      // eslint-disable-next-line no-console
      console.log('Error during entity dashboard click event!')
    }
  }

  private generatePasscodeEvent () {
    this.$refs.generatePasscodeDialog.open()
  }

  private get isThereAnAffiliatedAccount (): boolean {
    return !!this.affiliatedOrg?.name
  }
}
</script>
<style lang="scss" scoped>
  @import '$assets/scss/theme.scss';

  .account-color-empty {
    color: var(--v-error-base) !important;
  }

</style>
